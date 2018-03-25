class Logger:
    # 显示颜色格式：\033[显示方式;字体色;背景色m......[\033[0m]
    # 显示方式共6种
    default     = '0'     # 默认显示
    highlight   = '1'     # 高亮
    underline   = '4'     # 下划线
    blink       = '5'     # 闪烁
    rever_color = '7'     # 反显
    unhidden    = '8'     # 消隐
    # 字体颜色共7种
    BLACK       = '30'    # 设置字体色：黑色
    RED         = '31'    # 设置字体色：红色
    GREEN       = '32'    # 设置字体色：绿色
    YELLOW      = '33'    # 设置字体色：黄色
    BLUE        = '34'    # 设置字体色：蓝色
    PURPLE      = '35'    # 设置字体色：紫色
    DARKGREEN   = '36'    # 设置字体色：深绿色
    WHITE       = '37'    # 设置字体色：白色
    # 背景颜色共7种
    BBLACK       = '40'    # 设置背景色：黑色
    BRED         = '41'    # 设置背景色：红色
    BGREEN       = '42'    # 设置背景色：绿色
    BYELLOW      = '43'    # 设置背景色：黄色
    BBLUE        = '44'    # 设置背景色：蓝色
    BPURPLE      = '45'    # 设置背景色：紫色
    BDARKGREEN   = '46'    # 设置背景色：深绿色
    BWHITE       = '47'    # 设置背景色：白色

    HEADER = '\033['
    ENDC = '\033[0m'
    INFO = '\033[0;37;40m'      # 默认，白色黑底
    OK = '\033[1;32;40m'        # 高亮，绿色黑底
    WARNING = '\033[1;31;43m'   # 高亮，红色黄底
    ERROR = '\033[1;33;41m'     # 高亮，黄色红底
    

    @staticmethod
    def info(info):
        print(Logger.INFO + info + Logger.ENDC)

    @staticmethod
    def ok(info):
        print(Logger.OK + "[INFO] " + info + Logger.ENDC)

    @staticmethod
    def warn(info):
        print(Logger.WARNING + "[WARNING] " +  info + Logger.ENDC)

    @staticmethod
    def error(info):
        print(Logger.ERROR + "[ERROR] " + info + Logger.ENDC)

    @staticmethod
    def customize(info, mode = 0, fontcolor = 37, backcolor = 40):
        print(Logger.HEADER + str(mode) + ";" + str(fontcolor) + ";" + str(backcolor) + "m" + info + Logger.ENDC)
