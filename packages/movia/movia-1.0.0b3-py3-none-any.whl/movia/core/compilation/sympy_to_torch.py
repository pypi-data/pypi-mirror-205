#!/usr/bin/env python3

"""
** An adaptation of ``sympy.lambdify`` for torch. **
----------------------------------------------------
"""

import itertools
import numbers
import tokenize
import typing

from sympy.core.basic import Basic
from sympy.core.containers import Tuple
from sympy.core.symbol import Symbol
from sympy.core.sympify import sympify
from sympy.core.numbers import NumberSymbol
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication
from sympy.printing.pretty.pretty import pretty
from sympy.simplify.cse_main import cse
import torch



def _expr_to_atomic(expr: Basic, *, _symbols=None) -> list[tuple[Symbol, Basic]]:
    """
    ** Apply ``cse`` and split the sub patterns. **

    Parameters
    ----------
    expr : sympy.core.basic.Basic
        The sympy expression to split.

    Returns
    -------
    replacements : list of (Symbol, expression) pairs
        All of the common subexpressions that were replaced.
        All subexpressions are atomic.

    Examples
    --------
    >>> from pprint import pprint
    >>> from sympy.abc import x, y, z
    >>> from sympy.functions.elementary.trigonometric import sin
    >>> from movia.core.compilation.sympy_to_torch import _expr_to_atomic
    >>> exp = (x + y + z - 1)**2 * ((x + y + z)/(x + 1) + (x + y + z - 1)**2) * (x + 1)**(x + y + z)
    >>> pprint(_expr_to_atomic(exp)) # case cse and sub-patterns
    [(_0, x + y + z),
     (_4, _0 - 1),
     (_1, _4**2),
     (_2, x + 1),
     (_5, _2**_0),
     (_8, 1/_2),
     (_7, _0*_8),
     (_6, _1 + _7),
     (_3, _1*_5*_6)]
    >>> pprint(_expr_to_atomic(sin(sin(sin(1))))) # case replace in func
    [(_2, sin(1)), (_1, sin(_2)), (_0, sin(_1))]
    >>>
    """
    if _symbols is None:
        _symbols = iter(Symbol(f"_{i}") for i in itertools.count())
        rep, final = cse(
            expr, symbols=_symbols, optimizations="basic", order="canonical", list=False
        )
        rep.append((next(_symbols), final))
    else: # if cse is already called
        rep = [(next(_symbols), expr)]

    atom_rep = []
    for var, sub_expr in rep:
        if sub_expr.is_Atom:
            atom_rep.append((var, sub_expr))
            continue
        subs = {}
        for arg in sub_expr.args:
            if not arg.is_Atom:
                atom_rep += _expr_to_atomic(arg, _symbols=_symbols)
                subs[arg] = atom_rep[-1][0]
        if subs:
            sub_expr = sub_expr.xreplace(subs)
        atom_rep.append((var, sub_expr))
    return atom_rep


def _parse_expr(expr: typing.Union[Basic, numbers.Complex, str]) -> Basic:
    """
    ** Converts the expression in sympy compilable expression. **

    Parameters
    ----------
    expr : str or sympy.Expr
        The string representation of the equation.
        Some operators like multiplication can be implicit.

    Returns
    -------
    sympy.core.expr.Expr
        The version sympy of the expression.

    Raises
    ------
    SyntaxError
        If the entered expression does not allow to properly define an equation.

    Examples
    --------
    >>> from movia.core.compilation.sympy_to_torch import _parse_expr
    >>> _parse_expr(0)
    0
    >>> _parse_expr("1/2 + 1/2*cos(2pi(t - i*j))")
    cos(pi*(-2*i*j + 2*t))/2 + 1/2
    >>>
    """
    if isinstance(expr, str):
        transformations = standard_transformations + (implicit_multiplication,)
        try:
            expr = parse_expr(
                expr, transformations=transformations, evaluate=True
            )
        except (tokenize.TokenError, TypeError) as err:
            raise SyntaxError(f"failed to parse {expr}") from err
    elif isinstance(expr, numbers.Complex):
        expr = sympify(expr, evaluate=True)
    if not isinstance(expr, Basic):
        raise SyntaxError(f"need to be expression, not {expr.__class__.__name__}")
    return expr


def _release_variable_inplace(expr: Basic) -> list[tuple[Symbol, typing.Optional[Basic]]]:
    """
    ** Call ``_expr_to_atomic`` and optimise the memory. **

    Parameters
    ----------
    expr : sympy.core.basic.Basic
        Forwarded to ``_expr_to_atomic``.

    Returns
    -------
    replacements : list of (Symbol, expression or None) pairs
        All of the common subexpressions that were replaced.
        All subexpressions are atomic or None if the variable is not more used.

    Examples
    --------
    >>> from pprint import pprint
    >>> from sympy.abc import x, y, z
    >>> from movia.core.compilation.sympy_to_torch import _release_variable_inplace
    >>> from sympy.functions.elementary.trigonometric import sin
    >>> exp = (x + y + z - 1)**2 * ((x + y + z)/(x + 1) + (x + y + z - 1)**2) * (x + 1)**(x + y + z)
    >>> pprint(_release_variable_inplace(exp))
    [(y, x + y + z),
     (z, None),
     (_4, y - 1),
     (_4, _4**2),
     (x, x + 1),
     (_5, x**y),
     (x, 1/x),
     (x, x*y),
     (y, None),
     (x, _4 + x),
     (_4, _4*_5*x)]
    >>> pprint(_release_variable_inplace(sin(sin(sin(1)))))
    [(_2, sin(1)), (_2, sin(_2)), (_2, sin(_2))]
    >>>
    """
    rep = _expr_to_atomic(expr)
    i = 0
    while i < len(rep):
        symb, expr = rep[i]
        if unused := sorted(
            (s for s in expr.free_symbols if all(s not in e.free_symbols for _, e in rep[i+1:])),
            key=str,
        ):
            rep[i] = (unused[0], expr)
            rep[i+1:] = [(s, e.xreplace({symb: unused[0]})) for s, e in rep[i+1:]]
            if i + 1 != len(rep):
                for symb in unused[1:]:
                    rep.insert(i+1, (symb, None))
                    i += 1
        i += 1
    return rep


class LambdifyTorch:
    '''
    ** Convert a SymPy expression into a function that allows for fast torch numeric evaluation. **

    Examples
    --------
    >>> import torch
    >>> from sympy.abc import x, y, z
    >>> from movia.core.compilation.sympy_to_torch import LambdifyTorch
    >>> LambdifyTorch(x, x + 1)(torch.tensor(1.0))
    tensor(2.)
    >>> exp = (x + y + z - 1)**2 * ((x + y + z)/(x + 1) + (x + y + z - 1)**2) * (x + 1)**(x + y + z)
    >>> print(LambdifyTorch([x, y, z], exp))
    def lambdify(x, y, z):
        """
        ** Autogenerated function for fast torch evaluation. **
    <BLANKLINE>
                 x + y + z ⎛                 2   x + y + z⎞                  2
        (x + 1.0)         ⋅⎜(x + y + z - 1.0)  + ─────────⎟⋅(x + y + z - 1.0)
                           ⎝                      x + 1.0 ⎠
        """
        y += x
        y += z
        del z
        _4 = torch.tensor(-1.0, dtype=torch.float64) + y
        _4 **= 2
        x += 1.0000000000000000000000000000000
        _5 = x**y
        x **= -1
        x *= y
        del y
        x += _4
        _4 *= _5
        _4 *= x
        return _4
    >>>
    '''

    def __init__(self, args: typing.Union[Symbol, list[Symbol]], expr: Basic):
        """
        Parameters
        ----------
        args : sympy.Symbol or list[sympy.Symbol]
            A variable or a list of variables whose nesting represents the
            nesting of the arguments that will be passed to the function.
        expr : sympy.Expr
            An expression or list of expressions to be evaluated.
        """
        if isinstance(args, Symbol):
            args = [args]
        assert isinstance(args, list), args.__class__.__name__
        assert all(isinstance(a, Symbol) for a in args), args
        assert isinstance(expr, Basic), expr.__class__.__name__
        assert expr.free_symbols.issubset(set(args)), expr.free_symbols - set(args)
        expr = expr.subs({s: s.evalf(n=32) for s in expr.atoms(NumberSymbol)})
        expr = Tuple(*(a.evalf(32) for a in expr)) if isinstance(expr, Tuple) else expr.evalf(32)
        graph = _release_variable_inplace(expr)
        self._body = "\n".join(self._print(e, s) for s, e in graph)
        self._funcstr = (
            f"def lambdify({', '.join(str(s) for s in args)}):\n"
            + '    """\n'
            + "    ** Autogenerated function for fast torch evaluation. **\n"
            + "    \n    "
            + "\n    ".join(
                line.rstrip() for line in pretty(expr, use_unicode=None, num_columns=96).split("\n")
            )
            + '\n    """\n    '
            + "\n    ".join(self._body.split("\n"))
            + f"\n    return {graph[-1][0]}"
        )
        func_code = compile(self._funcstr, filename="", mode="exec")
        context = {"torch": torch}
        exec(func_code, context, context) # load the references in context, not in locals()
        self._func = context["lambdify"]

    def __call__(self, *args):
        return self._func(*args)

    def __str__(self):
        return self._funcstr

    @property
    def body(self) -> str:
        """
        ** The content of the function. **
        """
        return self._body

    def _print(self, expr: Basic, alloc: typing.Optional[Symbol]=None) -> str:
        """
        ** Convert the sympy expr in torch operation. **

        Returns
        -------
        operation : str
            The torch operation with the allocation, can be multiline.
        """
        if expr is None:
            return f"del {alloc}"
        if expr.is_real:
            val = f"torch.tensor({float(expr)}, dtype=torch.float64)"
            return val if alloc is None else f"{alloc} = {val}"
        if expr.is_complex:
            val = f"torch.tensor({complex(expr)}, dtype=torch.complex128)"
            return val if alloc is None else f"{alloc} = {val}"
        if expr.is_symbol:
            return str(expr) if alloc is None else f"{alloc} = {expr}"
        if (printer:= getattr(self, f"_print_{expr.__class__.__name__.lower()}", None)) is None:
            raise NotImplementedError(f"no printer for {expr}, class {expr.__class__.__name__}")
        return printer(expr, alloc)

    def _print_add(self, expr: Basic, alloc: typing.Optional[Symbol]=None) -> str:
        """
        >>> from sympy.abc import x
        >>> from movia.core.compilation.sympy_to_torch import LambdifyTorch
        >>> print(LambdifyTorch([x], 1 + x).body)
        x += 1.0000000000000000000000000000000
        >>>
        """
        if alloc in expr.args:
            val = ""
            alloc_found_in_pattern = False
            for pat in expr.args:
                if not alloc_found_in_pattern and pat == alloc:
                    alloc_found_in_pattern = True
                    continue
                if pat.is_number:
                    val += f"{alloc} += {pat}\n"
                else:
                    val += f"{alloc} += {self._print(pat)}\n"
            return val[:-1]
        val = " + ".join(self._print(a) for a in expr.args)
        return val if alloc is None else f"{alloc} = {val}"

    def _print_atan(self, expr: Basic, alloc: typing.Optional[Symbol]=None) -> str:
        """
        >>> from sympy.abc import x
        >>> from sympy.functions.elementary.trigonometric import atan
        >>> from movia.core.compilation.sympy_to_torch import LambdifyTorch
        >>> print(LambdifyTorch([x], atan(x)).body)
        x = torch.atan(x, out=x)
        >>>
        """
        if alloc is expr.args[0]:
            val = f"torch.atan({self._print(expr.args[0])}, out={alloc})"
        else:
            val = f"torch.atan({self._print(expr.args[0])})"
        return val if alloc is None else f"{alloc} = {val}"

    def _print_cos(self, expr: Basic, alloc: typing.Optional[Symbol]=None) -> str:
        """
        >>> from sympy.abc import x
        >>> from sympy.functions.elementary.trigonometric import cos
        >>> from movia.core.compilation.sympy_to_torch import LambdifyTorch
        >>> print(LambdifyTorch([x], cos(x)).body)
        x = torch.cos(x, out=x)
        >>>
        """
        if alloc is expr.args[0]:
            val = f"torch.cos({self._print(expr.args[0])}, out={alloc})"
        else:
            val = f"torch.cos({self._print(expr.args[0])})"
        return val if alloc is None else f"{alloc} = {val}"

    def _print_exp(self, expr: Basic, alloc: typing.Optional[Symbol]=None) -> str:
        """
        >>> from sympy.abc import x
        >>> from sympy.functions.elementary.trigonometric import exp
        >>> from movia.core.compilation.sympy_to_torch import LambdifyTorch
        >>> print(LambdifyTorch([x], exp(x)).body)
        x = torch.exp(x, out=x)
        >>>
        """
        if alloc is expr.args[0]:
            val = f"torch.exp({self._print(expr.args[0])}, out={alloc})"
        else:
            val = f"torch.exp({self._print(expr.args[0])})"
        return val if alloc is None else f"{alloc} = {val}"

    def _print_infinity(self, _, alloc: typing.Optional[Symbol]=None) -> str:
        """
        >>> from sympy.core.numbers import Infinity
        >>> from movia.core.compilation.sympy_to_torch import LambdifyTorch
        >>> print(LambdifyTorch([], Infinity()).body)
        _0 = torch.tensor(torch.inf, dtype=torch.float64)
        >>>
        """
        val = "torch.tensor(torch.inf, dtype=torch.float64)"
        return val if alloc is None else f"{alloc} = {val}"

    def _print_mul(self, expr: Basic, alloc: typing.Optional[Symbol]=None) -> str:
        """
        >>> from sympy.abc import x
        >>> from movia.core.compilation.sympy_to_torch import LambdifyTorch
        >>> print(LambdifyTorch([x], 2*x).body)
        x *= 2.0000000000000000000000000000000
        >>> print(LambdifyTorch([x], -x).body)
        x = torch.neg(x, out=x)
        >>>
        """
        if alloc in expr.args:
            val = ""
            alloc_found_in_pattern = False
            for pat in expr.args:
                if not alloc_found_in_pattern and pat == alloc:
                    alloc_found_in_pattern = True
                    continue
                if pat == -1:
                    val += f"{alloc} = torch.neg({alloc}, out={alloc})\n"
                elif pat.is_number:
                    val += f"{alloc} *= {pat}\n"
                else:
                    val += f"{alloc} *= {self._print(pat)}\n"
            return val[:-1]
        val = " * ".join(self._print(a) for a in expr.args)
        return val if alloc is None else f"{alloc} = {val}"

    def _print_nan(self, _, alloc: typing.Optional[Symbol]=None) -> str:
        """
        >>> from sympy.core.numbers import NaN
        >>> from movia.core.compilation.sympy_to_torch import LambdifyTorch
        >>> print(LambdifyTorch([], NaN()).body)
        _0 = torch.tensor(torch.nan, dtype=torch.float64)
        >>>
        """
        val = "torch.tensor(torch.nan, dtype=torch.float64)"
        return val if alloc is None else f"{alloc} = {val}"

    def _print_negativeinfinity(self, _, alloc: typing.Optional[Symbol]=None) -> str:
        """
        >>> from sympy.core.numbers import NegativeInfinity
        >>> from movia.core.compilation.sympy_to_torch import LambdifyTorch
        >>> print(LambdifyTorch([], NegativeInfinity()).body)
        _0 = torch.tensor(-torch.inf, dtype=torch.float64)
        >>>
        """
        val = "torch.tensor(-torch.inf, dtype=torch.float64)"
        return val if alloc is None else f"{alloc} = {val}"

    def _print_pow(self, expr: Basic, alloc: typing.Optional[Symbol]=None) -> str:
        """
        >>> from sympy.abc import x
        >>> from movia.core.compilation.sympy_to_torch import LambdifyTorch
        >>> print(LambdifyTorch([x], x**2).body)
        x **= 2
        >>> print(LambdifyTorch([x], 1/x).body)
        x **= -1
        >>> print(LambdifyTorch([x], x**(1/2)).body)
        x = torch.sqrt(x, out=x)
        >>>
        """
        base, exp = expr.as_base_exp()
        if alloc == base:
            if exp == .5:
                return f"{alloc} = torch.sqrt({alloc}, out={alloc})"
            if exp.is_number:
                return f"{alloc} **= {exp}"
            return f"{alloc} **= {self._print(exp)}"
        if exp == .5:
            val = f"torch.sqrt({base})"
        elif exp == -.5:
            val = f"1/torch.sqrt({base})"
        elif exp.is_number:
            val = f"{self._print(base)}**{exp}"
        else:
            val = f"{self._print(base)}**{self._print(exp)}"
        return val if alloc is None else f"{alloc} = {val}"

    def _print_sin(self, expr: Basic, alloc: typing.Optional[Symbol]=None) -> str:
        """
        >>> from sympy.abc import x
        >>> from sympy.functions.elementary.trigonometric import sin
        >>> from movia.core.compilation.sympy_to_torch import LambdifyTorch
        >>> print(LambdifyTorch([x], sin(x)).body)
        x = torch.sin(x, out=x)
        >>>
        """
        if alloc is expr.args[0]:
            val = f"torch.sin({self._print(expr.args[0])}, out={alloc})"
        else:
            val = f"torch.sin({self._print(expr.args[0])})"
        return val if alloc is None else f"{alloc} = {val}"

    def _print_tuple(self, expr: Basic, alloc: typing.Optional[Symbol]=None) -> str:
        """
        >>> from sympy.abc import x
        >>> from sympy.core.containers import Tuple
        >>> from movia.core.compilation.sympy_to_torch import LambdifyTorch
        >>> print(LambdifyTorch([], Tuple()).body)
        _0 = ()
        >>> print(LambdifyTorch([x], Tuple(x)).body)
        x = (x,)
        >>> print(LambdifyTorch([x], Tuple(x, x)).body)
        x = (x, x)
        >>>
        """
        if len(expr) == 0:
            val = "()"
        elif len(expr) == 1:
            val = f"({self._print(expr[0])},)"
        else:
            val = f"({', '.join(self._print(a) for a in expr)})"
        return val if alloc is None else f"{alloc} = {val}"


class LambdifyHomogeneous(LambdifyTorch):
    """
    ** Like LambdifyTorch accepting list and tuple as input. **

    Examples
    --------
    >>> import torch
    >>> from sympy.abc import x
    >>> from movia.core.compilation.sympy_to_torch import LambdifyHomogeneous
    >>> LambdifyHomogeneous(x, x * (x+1))(torch.tensor(1.0))
    tensor(2., dtype=torch.float64)
    >>> LambdifyHomogeneous(x, [x, x+1])(torch.tensor(1.0))
    [tensor(1.), tensor(2., dtype=torch.float64)]
    >>> LambdifyHomogeneous(x, (x, x+1))(torch.tensor(1.0))
    (tensor(1.), tensor(2., dtype=torch.float64))
    >>>
    """

    def __init__(self,
        args: typing.Union[Symbol, list[Symbol]],
        expr: typing.Union[Basic, list[Basic], tuple[Basic]]
    ):
        if isinstance(expr, tuple):
            self.kind = tuple
            expr = Tuple(*expr)
        elif isinstance(expr, list):
            self.kind = list
            expr = Tuple(*expr)
        else:
            self.kind = Basic
        super().__init__(args, expr)

    def __call__(self, *args):
        res = super().__call__(*args)
        if self.kind is not Basic:
            res = self.kind(res)
        return res
