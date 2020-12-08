import colorama

colorama.init()


class Effect:
    name = 'Effect'

    def __init__(self, hero, duration):
        self.hero = hero
        self.duration = duration

    def before_move_tick(self):
        pass

    def after_move_tick(self):
        pass

    def on_ending(self):
        pass

    def decrease_duration(self):
        self.duration -= 1
        print(f'{self.name} тікнув. Залишилося {self.duration} ходів.')
        if self.duration == 0:
            self.die()

    def die(self):
        print(f"{self.name} закінчився.")
        self.on_ending()
        self.hero.effects.remove(self)

    def __str__(self):
        return f"{self.name} ({self.duration} ходів)"


class Poisoning(Effect):
    name = 'Отруєння'

    def __init__(self, hero, duration, damage):
        super().__init__(hero, duration)
        self.damage = damage

    def before_move_tick(self):
        print(f"{colorama.Fore.GREEN}Отруєння в ділі{colorama.Fore.RESET}")
        self.hero.loose_hp(self.damage)
        self.decrease_duration()

    def __str__(self):
        return f"{colorama.Fore.GREEN}{self.name}{colorama.Fore.RESET} ({self.duration} ходів {self.damage} урона)"


class Bleeding(Effect):
    name = 'Кровотеча'

    def calculate_damage(self):
        if 1 <= self.hero.max_hp <= 9:
            return 1
        elif 10 <= self.hero.max_hp <= 19:
            return 2
        elif 20 <= self.hero.max_hp <= 29:
            return 3
        elif 30 <= self.hero.max_hp <= 39:
            return 4
        else:
            return 5

    def after_move_tick(self):
        print(f"{colorama.Fore.RED}Кровотеча в ділі{colorama.Fore.RESET}")
        self.hero.loose_hp(self.calculate_damage())
        self.decrease_duration()


class Stun(Effect):
    name = 'Оглушення'

    def before_move_tick(self):
        self.hero.can_do_move = False
        self.decrease_duration()


class Regeneration(Effect):
    name = "Регенерація"

    def __init__(self, hero, duration, hp):
        super().__init__(hero, duration)
        self.hp = hp

    def before_move_tick(self):
        self.hero.regen_hp(self.hp)
        self.decrease_duration()

    def __str__(self):
        return f"{colorama.Fore.GREEN}{self.name}{colorama.Fore.RESET} ({self.duration} ходів {self.hp} hp)"


class Fire(Effect):
    name = 'Підпалення'

    def __init__(self, hero, duration):
        super().__init__(hero, duration)
        self.damage = 1

    def after_move_tick(self):
        print(f"{colorama.Fore.GREEN}Підпалення в ділі{colorama.Fore.RESET}")
        self.hero.loose_hp(self.damage)
        self.decrease_duration()
        self.damage += 1

    def __str__(self):
        return f"{colorama.Fore.GREEN}{self.name}{colorama.Fore.RESET} ({self.duration} ходів {self.damage} урона)"
