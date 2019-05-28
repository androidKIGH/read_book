# 阅读获取金币
READ_G_TYPE = 0
# 观看激励视频获取金币
READ_REWARD_G_TYPE = 1

# 分享获取金币
SHARE_G_TYPE = 4
# 分享获取金币观看激励视频
SHARE_REWARD_G_TYPE = 5

# 转盘获取金币
WHELL_G_TYPE = 6
# 转盘获取金币观看激励视频
WHELL_REWARD_G_TYPE = 7

# 观看激励视频获取金币
TASK_REWARD_COIN = 20
#  app升级赠送金币
TASK_UPDATE_COIN = 21

# ------------///--------------------每日任务每天只做一次
# 签到获取金币观看激励视频
SIGN_REWARD_G_TYPE = 3

# ------------///--------------------新书任务只做一次
# 新手任务 - 查看用户手册
TASK_NEW_LOOK_RULE = 10
# 新手任务 - 查看用户手册激励视频
TASK_NEW_LOOK_REWARD_RULE = 11

# 新手任务 - 查看我的金币
TASK_NEW_LOOK_CION = 12
# 新手任务 - 查看我的金币激励视频
TASK_NEW_LOOK_REWARD_CION = 13

# 新人福利
TASK_NEW_NEW_WELFACE = 14

TASK_FILL_QUESTIONS = 15

TASK_FILL_QUESTIONS_REWARD_COIN = 16


# 新手任务 一个用户只能做一次的任务
new_user_task = [TASK_NEW_LOOK_RULE, TASK_NEW_LOOK_REWARD_RULE,
                 TASK_NEW_LOOK_CION, TASK_NEW_LOOK_REWARD_CION,
                 TASK_NEW_NEW_WELFACE,
                 TASK_FILL_QUESTIONS, TASK_FILL_QUESTIONS_REWARD_COIN]
# 日常任务 每天只能做一次的任务
daily_task = [SIGN_REWARD_G_TYPE]

# 普通任务
normal_task = [READ_G_TYPE, READ_REWARD_G_TYPE,
               SHARE_G_TYPE, WHELL_G_TYPE,
               SHARE_REWARD_G_TYPE, WHELL_REWARD_G_TYPE,
               TASK_REWARD_COIN, TASK_UPDATE_COIN]

# 次数任务 每天没可做有次数限制
# times_task = [SHARE_G_TYPE, WHELL_G_TYPE, SHARE_REWARD_G_TYPE, WHELL_REWARD_G_TYPE]
