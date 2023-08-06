"""Tado exceptions."""


class TadoException(Exception):
    """Base exception class for Tado."""


class TadoNotSupportedException(TadoException):
    """Exception to indicate a requested action is not supported by Tado."""

