class TgOutputAdapter:
    """
    Класс адаптер для преобразования python объектов,
    типа pydantic, dict, etc в str.
    """
    def __init__(
        self, data_to_tranform: dict | list[dict], 
        pattern: dict = None,
    ) -> None:
        self.data_to_tranform = data_to_tranform
        self.pattern = pattern

    def transform(self) -> str:
        
        if isinstance(self.data_to_tranform, list):

            result = []
            for data in self.data_to_tranform:
                
                result.append(
                    '\n'.join(f'{key}: {value}' for key, value in data.items())
                )
            return '\n\n'.join(result)
        
        return '\n'.join(
            f'{key}: {value}' for key, value in self.data_to_tranform.items()
        )

    