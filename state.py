class State:
    def __init__(self, state_manager):
        self.state_manager = state_manager

    def on_draw(self, surface):
        pass

    def on_event(self, event):
        pass

    def on_update(self, dt, ticks):
        pass
