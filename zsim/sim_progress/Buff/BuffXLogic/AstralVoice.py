from sim_progress.Buff import Buff, JudgeTools, check_preparation, find_tick


class AstralVoiceRecord:
    def __init__(self):
        self.equipper = None
        self.char = None
        self.trigger_buff_0 = None
        self.sub_exist_buff_dict = None
        self.action_stack = None


class AstralVoice(Buff.BuffLogic):
    """
    这是静听佳音四件套的生效逻辑。该Buff有一个“触发器”，
    该触发器由简单逻辑控制，会根据支援突击触发、叠层和刷新；
    而触发器本身并无效果，真正实现增伤和复杂判定的是本buff的逻辑模块。
    本模块由 复杂判定（xjudge）  和 复杂生效（xstart） 两个部分构成
    """

    def __init__(self, buff_instance):
        super().__init__(buff_instance)
        self.buff_instance = buff_instance
        self.xjudge = self.special_judge_logic
        self.xeffect = self.special_effect_logic
        self.equipper = None
        self.buff_0 = None
        self.record = None

    def get_prepared(self, **kwargs):
        return check_preparation(self.buff_0, **kwargs)

    def check_record_module(self):
        if self.equipper is None:
            self.equipper = JudgeTools.find_equipper("静听嘉音")
        if self.buff_0 is None:
            """
            这里的初始化，找到的buff_0实际上是佩戴者的buff_0，
            即使是在受益者的buff.history.record中存储的，也是装备佩戴者的buff_0。
            """
            self.buff_0 = JudgeTools.find_exist_buff_dict()[self.equipper][
                self.buff_instance.ft.index
            ]
        if self.buff_0.history.record is None:
            self.buff_0.history.record = AstralVoiceRecord()
        self.record = self.buff_0.history.record

    def special_judge_logic(self, **kwargs):
        """
        复杂判定逻辑：首先要检测触发器Buff的激活情况；
        即：trigger_buff_0.dy.active
        然后是对比trigger_buff_level，对比通过才能输出True
        """
        self.check_record_module()
        self.get_prepared(
            equipper="静听嘉音",
            trigger_buff_0=(
                self.buff_instance.ft.operator,
                "Buff-驱动盘-静听嘉音-嘉音",
            ),
            action_stack=1,
        )
        tick_now = JudgeTools.find_tick()

        skill_node = kwargs.get('skill_node', None)
        if skill_node is None:
            return False
        if self.record.trigger_buff_0.dy.active and skill_node.skill.trigger_buff_level == 7:
            if skill_node.loading_mission.mission_dict.get(tick_now, None) == 'start':

                return True
            else:
                return False
        else:
            return False

    def special_effect_logic(self, **kwargs):
        self.check_record_module()
        self.get_prepared(
            equipper="静听嘉音",
            trigger_buff_0=(
                self.buff_instance.ft.operator,
                "Buff-驱动盘-静听嘉音-嘉音",
            ),
            sub_exist_buff_dict=1,
        )
        tick_now = find_tick()
        self.buff_instance.simple_start(tick_now, self.record.sub_exist_buff_dict)
        self.buff_instance.dy.count = self.record.trigger_buff_0.dy.count
        self.buff_instance.update_to_buff_0(self.buff_0)
