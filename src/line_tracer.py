from time import sleep
from device import read_device
from ev3dev.auto import ColorSensor, TouchSensor

class LineTracer:
    u"""PID制御によるライントレース
    キャリブレーション後のカラーセンサー値を目標値として旋回量を制御
    現時点では前進速度は固定値を想定
    →走行速度によって係数を調整する必要があるため
    """

    def __init__(self, setting):
        # target_v 目標値
        # delta_t 周回時間
        self.refrection_target = 0.0
        self.delta_t = 0.025 # 10msec
        # TODO: P係数(要調整)
        # 8.5V - 0.31
        # 8.2V - 0.30
        # 7.5V - 0.26
        self.k_p = 0.26 #0.26
        # TODO: I係数(要調整)
        self.k_i = 0.1
        # TODO: D係数(要調整)
        self.k_d = 0.05
        # 前回偏差
        self.e_b = 0.0
        # 前回までの偏差値
        self.p_b = 0.0
        # 前回までの積分値
        self.i_b = 0.0
        # 前回までの微分値
        self.d_b = 0.0
        # 前回値
        #self.previous_refrection_raw = [0 for _ in range(5) ]
        self.previous_refrection_raw = 0

        self.color = ColorSensor()
        self.color.mode = self.color.MODE_REF_RAW #raw値
        self.color_reflection_fd = open(self.color._path + "/value0", "rb")

        white_target = setting['lineWhiteLuminance']
        black_target = setting['lineBlackLuminance']
        target_white_rate = setting['lineLuminanceRate']

        self.refrection_target = (white_target * target_white_rate) + (black_target * (1.0 - target_white_rate))
        self.previous_refrection_raw = self.refrection_target

    def calibrate_color_sensor(self):
        color_val = 0
        gyro_rate_calibrate_count = 100

        touch = TouchSensor()

        print('-- SET ON WHITE COLOR LINE --')
        while not touch.is_pressed:
            sleep(0.1)

        for _ in range(gyro_rate_calibrate_count):
            color_val = read_device(self.color_reflection_fd)
            white_target = white_target + color_val
            #pushPrevious(color_val)
            sleep(0.01)
        white_target = white_target / gyro_rate_calibrate_count

        print('-- SET ON BLACK COLOR LINE --')
        while not touch.is_pressed:
            sleep(0.1)

        for _ in range(gyro_rate_calibrate_count):
            color_val = read_device(self.color_reflection_fd)
            black_target = black_target + color_val
            #pushPrevious(color_val)
            sleep(0.01)
        black_target = black_target / gyro_rate_calibrate_count

        print('White Color: {}'.format(white_target))
        print('Black Color: {}'.format(black_target))

        #目標値を保管
        self.refrection_target = (white_target * target_white_rate) + (black_target * (1.0 - target_white_rate))
        self.previous_refrection_raw = self.refrection_target

        u"""
        def pushPrevious(self, val)
        self.previous[0] = self.previous[1]
        self.previous[1] = self.previous[2]
        self.previous[2] = self.previous[3]
        self.previous[3] = self.previous[3]
        self.previous[4] = val
        """

    def line_tracing(self):
        u""" 速度、旋回値をpwm値として返却 """
        #センサー値を取得
        refrection_raw = read_device(self.color_reflection_fd)
        ref_avarage = int(round((self.previous_refrection_raw + refrection_raw) / 2))
        self.previous_refrection_raw = refrection_raw

        #指示値を取得
        direction = self.__calc_direction(ref_avarage)

        # NOTE: 旋回値の大きさを考慮し、段階的に走行速度を決定するアルゴリズムを考えた。
        # パラメータは
        # - direction: 旋回デューティ比
        # - speed: 走行速度デューティ比
        # - a_r:
        if direction < -13 or direction > 13:
            # 低速値
            # NOTE: 倒れなければ速度を下げる必要がない。倒れない程度に速度を上げる方向で調整。30は7.5Vの時にちょうどよさそう
            speed = 40
            # NOTE: directionの条件は調整中。 コースアウトする場合は、ここの値を小さくするとよい。
            # NOTE: 逆に直線で遅くなる傾向にあれば上げるべき。
        elif direction < -9 or direction > 9:
            # 中速値
            # NOTE: コースアウトする場合、下げる必要がある。コースアウトしない程度に速度を上げる方向で調整。60はまだ決まった値ではない。
            speed = 75
        else:
            # 高速値
            # NOTE: できるだけ上げたい値。90でちょうどよさそう。7.5Vの時。
            speed = 82

        # NOTE: ライン左端を基準に走行させるために、旋回方向を - で反転している
        return speed, -direction, refrection_raw

    def shutdown(self):
        self.color_reflection_fd.close()

    def __calc_direction(self, brightness):
        u"""旋回量取得"""
        # error 偏差
        # p_n P制御
        # i_n I制御
        # d_n D制御

        # pid演算
        error = self.refrection_target - brightness
        p_n = self.k_p * error
        integral = (self.i_b + ((error + self.e_b) / 2.0 * self.delta_t))
        i_n = self.k_i * integral
        d_n = self.k_d * (error - self.e_b) / self.delta_t
        direction = (p_n + i_n + d_n)

        # -100 ～100に収める
        if direction > 100:
            direction = 100
        elif direction < -100:
            direction = -100

        # 値の保存
        self.e_b = error
        self.p_b = p_n
        self.i_b = integral
        self.d_b = d_n

        return direction
