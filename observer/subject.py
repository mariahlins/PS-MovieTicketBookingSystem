class Subject:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        """Adiciona um novo observer para ser notificado de eventos."""
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer):
        """Remove um observer da lista de notificação."""
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self, event_type, data):
        """Notifica todos os observers sobre um evento específico."""
        for observer in self._observers:
            observer.update(event_type, data)
