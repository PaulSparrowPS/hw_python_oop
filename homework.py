M_IN_KM = 1000
LEN_STEP = 0.65


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """возвращает строку сообщения"""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000.000
    LEN_STEP = 0.650
    MIN_IN_H: float = 60.000

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
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18.000
    CALORIES_MEAN_SPEED_SHIFT: float = 1.790
    KMH_IN_MS: float = 0.2780
    LEN_STEP: float = 0.650
    M_IN_KM: float = 1000.000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        super().__init__(action, duration, weight)
        super().get_distance()
        super().get_mean_speed()
        super().show_training_info()

    def get_distance(self) -> float:
        """Расчёт дистанции, которую пользователь преодолел за тренировку"""
        return super().get_distance()

    def geat_mean_speed(self) -> float:
        """Расчёт средней скорости движения во время тренировки"""
        return super().geat_mean_speed()

    def get_spent_calories(self) -> float:
        """Расчёт количества калорий, израсходованных за тренировку"""
        spent_calories = ((super().get_mean_speed()
                          * self.CALORIES_MEAN_SPEED_MULTIPLIER
                          + self.CALORIES_MEAN_SPEED_SHIFT)
                          * self.weight / self.duration * self.M_IN_KM)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 0.035
    CALORIES_MEAN_SPEED_SHIFP = 0.029
    M_IN_KM: int = 1000.000
    LEN_STEP: float = 0.650
    MIN_IN_H: float = 60.000
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: float = 100.000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        super().get_distance()
        super().get_mean_speed()
        super().show_training_info()

    def get_spent_calories(self) -> float:
        """Расчёт количества калорий, израсходованных за тренировку"""
        spent_calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                          * self.weight
                          + (super().get_mean_speed() *self.KMH_IN_MSEC) ** 2
                          / (self.height / self.CM_IN_M)
                          * self.CALORIES_MEAN_SPEED_SHIFP * self.weight)
                          * (self.duration * self.MIN_IN_H))
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 1.100
    CALORIES_MEAN_SPEED_SHIFP = 2.000
    LEN_STEP: int = 1.380
    M_IN_KM: float = 1000.000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 lenght_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.lenght_pool = lenght_pool
        self.count_pool = count_pool
        super().get_distance()
        super().show_training_info()

    def get_spent_calories(self) -> float:
        """Расчёт количества калорий, израсходованных за тренировку"""
        spent_calories = ((super().get_mean_speed()
                          + self.CALORIES_MEAN_SPEED_SHIFP)
                          * self.CALORIES_MEAN_SPEED_MULTIPLIER
                          * self.weight * self.duration)
        return spent_calories

    def get_mean_speed(self) -> float:
        """Расчёт средней скорости движения во время тренировки"""
        return (self.lenght_pool * self.count_pool
                / self.M_IN_KM / self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    data_pack: dict[str, type[Training]] = {'SWM': Swimming,
                                            'RUN': Running,
                                            'WLK': SportsWalking}
    class_tra: Training = data_pack[workout_type](*data)
    return class_tra


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
