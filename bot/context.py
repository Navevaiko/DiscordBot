import contextvars

gameContext = contextvars.ContextVar('game', default=None)