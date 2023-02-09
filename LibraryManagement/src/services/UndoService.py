class UndoService:
    def __init__(self, book_service, client_service, rentals_service):
        self._book_service = book_service
        self._client_service = client_service
        self._rentals_service = rentals_service
        self._undo_operations = []
        self._undo_reversed_operations = []
        self._undo_index = -1
        self._redo_operations = []
        self._redo_reversed_operations = []
        self._redo_index = -1
        self._undo_cascade = []
        self._undo_cascade_reversed = []
        self._redo_cascade = []
        self._redo_cascade_reversed = []

    def record_undo_cascade(self, operation):
        self._undo_cascade.append(operation)

    def record_undo_cascade_reversed(self, operation):
        self._undo_cascade_reversed.append(operation)

    def record_undo_operation(self, operation):
        self._undo_operations.append(operation)
        self._undo_index += 1

    def record_reversed_operation(self, operation):
        self._undo_reversed_operations.append(operation)

    def restore_redo(self):
        self._redo_index = -1
        self._redo_reversed_operations.clear()
        self._redo_cascade.clear()
        self._redo_cascade_reversed.clear()
        self._redo_operations.clear()

    def undo(self):
        if self._undo_index == -1:
            print("Can't undo anymore!")
            return
        undo_op = self._undo_operations[self._undo_index]
        redo_op = self._undo_reversed_operations[self._undo_index]
        undo_cascades = self._undo_cascade[self._undo_index]
        redo_cascades = self._undo_cascade_reversed[self._undo_index]
        self._redo_cascade_reversed.append(undo_cascades)
        self._redo_cascade.append(redo_cascades)
        self._undo_cascade.pop(self._undo_index)
        self._undo_cascade_reversed.pop(self._undo_index)
        self._redo_reversed_operations.append(undo_op)
        self._redo_operations.append(redo_op)
        self._redo_index += 1
        self._undo_operations.pop(self._undo_index)
        self._undo_reversed_operations.pop(self._undo_index)
        self._undo_index -= 1
        for i in undo_cascades:
            if type(i) is not list:
                i.call()
        if type(undo_op) is not list:
            undo_op.call()

    def redo(self):
        if self._redo_index == -1:
            print("Can't redo anymore!")
            return
        redo_op = self._redo_operations[self._redo_index]
        undo_op = self._redo_reversed_operations[self._redo_index]
        redo_cascades = self._redo_cascade[self._redo_index]
        undo_cascades = self._redo_cascade_reversed[self._redo_index]
        self._undo_cascade_reversed.append(redo_cascades)
        self._undo_cascade.append(undo_cascades)
        self._redo_cascade.pop(self._redo_index)
        self._redo_cascade_reversed.pop(self._redo_index)
        self._undo_reversed_operations.append(redo_op)
        self._undo_operations.append(undo_op)
        self._undo_index += 1
        self._redo_operations.pop(self._redo_index)
        self._redo_reversed_operations.pop(self._redo_index)
        self._redo_index -= 1
        for i in redo_cascades:
            if type(i) is not list:
                i.call()
        if type(redo_op) is not list:
            redo_op.call()


class FunctionCall:
    def __init__(self, function_name, *function_params):
        self._function_name = function_name
        self._function_params = function_params

    def call(self):
        self._function_name(*self._function_params)
