from dataclasses import asdict, dataclass
from typing import Dict, List

SWM = 'SWM'
RUN = 'RUN'
WLK = 'WLK'


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: str
    distance: str
    speed: str
    calories: str

    def get_message(self) -> str:
        return ("Тип тренировки: {training_type}; "
                "Длительность: {duration:.3f} ч.; "
                "Дистанция: {distance:.3f} км; "
                "Ср. скорость: {speed:.3f} км/ч; "
                "Потрачено ккал: {calories:.3f}.".format(**asdict(self)))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MINS_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        information_message = InfoMessage(self.__class__.__name__,
                                          self.duration,
                                          self.get_distance(),
                                          self.get_mean_speed(),
                                          self.get_spent_calories())
        return information_message


class Running(Training):
    """Тренировка: бег."""
    FIRST_CALORIE_INDEX: int = 18
    SECOND_CALORIE_INDEX: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.FIRST_CALORIE_INDEX * self.get_mean_speed()
                - self.SECOND_CALORIE_INDEX) * self.weight
                / self.M_IN_KM * (self.duration * self.MINS_IN_HOUR))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    THIRD_CALORIE_INDEX: float = 0.035
    FOURTH_CALORIE_INDEX: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.THIRD_CALORIE_INDEX * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.FOURTH_CALORIE_INDEX * self.weight)
                * (self.duration * self.MINS_IN_HOUR))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (self.get_mean_speed() + 1.1) * 2 * self.weight


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_types: Dict[str, List[int]] = {
        SWM: Swimming,
        RUN: Running,
        WLK: SportsWalking
    }
    if workout_type not in workout_types:
        raise ValueError('Неизвестный тип тренировки')
    return workout_types[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        (SWM, [720, 1, 80, 25, 40]),
        (RUN, [15000, 1, 75]),
        (WLK, [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
