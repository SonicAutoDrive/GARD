import threading
import queue


class kalman_filter_thread(threading.Thread):
    '''
    执行卡尔曼滤波的线程
    '''
    def __init__(self, threadID, name, queue_in, queue_out, freeze_count, activate, alpha=0, beta=0.001, chi=1, w=448, t_max=10, R0=0):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.queue_in = queue_in
        self.queue_out = queue_out
        self.alpha = alpha
        self.beta = beta
        self.chi = chi
        self.w = w
        self.t_max = t_max
        self.t = 0
        self.R0 = R0
        self.freeze_count = freeze_count
        self.activate = activate
        self.activate_lock = threading.Lock()


    def set_activate(self, value):
        with self.activate_lock:
            self.activate = value

    
    def run(self):
        def R(t):
            # 计算R值
            return self.R0 + self.alpha * t
        def Q(t):
            # 计算Q值
            return self.beta * self.w + self.chi * max(0, self.t_max - t)
        # iteration
        
        while True:
            self.set_activate(True)
            data = self.queue_in.get()
            # 结束条件
            if data == -1:
                return
            # 判断是否为新线程，如果是则初始化
            if not self.t:
                # 初始化，*_hat 代表最优估计 *(t|t)
                self.x_hat = data
                self.P_hat = 0    
            else:
                # 执行预测过程
                self.P = self.P_hat + Q(self.t + 1)
                self.x = self.x_hat
                # 根据测量值data进行修正
                K = self.P / (R(self.t + 1) + Q(self.t + 1))
                self.x_hat = self.x + K * (data - self.x)
                self.P_hat = (1 - K) * self.P
            ##print(self.name + ' get ' + str(data))
            self.queue_out.put(self.x_hat)
            self.t = self.t + 1
        