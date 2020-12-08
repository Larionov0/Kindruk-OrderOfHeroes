import random
import colorama
from os import system
import effects

colorama.init()
system('cls')


def my_round(num):
    return int(num + 0.5)


class Hero:
    name = 'Hero'
    hp = max_hp = 20
    attack = 3
    armor = 0
    magic = 0

    skill_1_name = "Skill1"
    skill_2_name = "Skill2"

    skill_1_description = ''
    skill_2_description = ''

    alive = True
    did_action = False
    can_do_move = True

    def __init__(self, team_number):
        self.team_number = team_number
        self.effects = []

    def colored_name(self):
        colors = {
            1: colorama.Fore.BLUE,
            2: colorama.Fore.RED
        }
        return colors[self.team_number] + self.name + colorama.Fore.RESET

    def normal_attack(self, other):
        print(f"{self.name} копнув героя {other.name}")
        other.get_damage(self.attack)

    def get_damage(self, damage):
        if damage > self.armor:
            remaining_damage = damage - self.armor
        else:
            remaining_damage = 1
        print(f"У {self.name} влітає {remaining_damage}/{damage} урона")
        self.loose_hp(remaining_damage)

    def regen_hp(self, hp):
        self.hp += hp
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        print(f"{self.colored_name()}{colorama.Fore.GREEN} полікувався на {hp} hp. Тепер {self.hp}/{self.max_hp}{colorama.Fore.RESET}")

    def loose_hp(self, damage):
        self.hp = self.hp - damage
        print(f"{self.name} втратив {damage} hp. Залишилося {self.hp}/{self.max_hp}")
        if self.hp <= 0:
            self.die()

    def die(self):
        self.alive = False
        print(f"{self.name} is dead")

    def cast_1_skill(self, my_team, enemies_team):
        pass

    def cast_2_skill(self, my_team, enemies_team):
        pass

    def before_move(self):
        self.did_action = False
        self.can_do_move = True
        for effect in self.effects:
            effect.before_move_tick()

    def after_move(self):
        for effect in self.effects:
            effect.after_move_tick()

    def make_move_menu(self, my_team, enemies_team):
        self.before_move()
        if self.can_do_move:
            while True:
                text = f'\n\n--= Хід героя {self.colored_name()} =--\n' \
                       f'a - звичайна атака\n' \
                       f'1 - використати 1 вміння\n' \
                       f'2 - використати 2 вміння\n' \
                       f'- - закінчити хід\n' \
                       f'i - подивитися інформацію про героїв\n' \
                       f'ваш вибір: '
                choice = input(text)
                if choice == 'a':
                    self.normal_attack_menu(enemies_team)
                elif choice == '1':
                    if self.did_action:
                        print("Ви вже використали дію")
                    else:
                        print(f"--= {self.skill_1_name} =--")
                        print(self.skill_1_description)
                        choice = input("Кастуєте скіл? (y/n): ")
                        if choice == 'y':
                            self.cast_1_skill(my_team, enemies_team)
                elif choice == '2':
                    if self.did_action:
                        print("Ви вже використали дію")
                    else:
                        print(f"--= {self.skill_2_name} =--")
                        print(self.skill_2_description)
                        choice = input("Кастуєте скіл? (y/n): ")
                        if choice == 'y':
                            self.cast_2_skill(my_team, enemies_team)
                elif choice == '-':
                    break
                elif choice == 'i':
                    self.print_heroes_info(my_team, enemies_team)
        else:
            print(f"{self.name} пропускає хід!")
        self.after_move()

    def print_heroes_info(self, my_team, enemies_team):
        print("Герои:")
        for hero in my_team + enemies_team:
            print("-" * 20)
            print(hero)
            print("-" * 20)
        input("<Enter>")

    def normal_attack_menu(self, enemies_team):
        if self.did_action:
            print(f"Ви вже атакували")
            return

        target_hero = self.choose_hero_from_list(enemies_team, "Виберіть героя для удару:")
        if target_hero is None:
            return
        self.normal_attack(target_hero)
        self.did_action = True

    def choose_hero_from_list(self, heroes_list, text='--= Виберіть героя =--'):
        """
        return:
        1. Hero, якщо герой був вибраний
        2. None, якщо герой не вибраний
        """
        print(text)
        print("0 - назад")
        for i, hero in enumerate(heroes_list):  # У і складається індекси, а у hero  - герої
            print(f"{i + 1} - {hero.colored_name()} ({hero.hp}/{hero.max_hp})")
        choice = input('Ваш вибір: ')
        if choice == '0':
            return None
        if choice.isdigit() and 0 < int(choice) <= len(heroes_list):
            hero = heroes_list[int(choice) - 1]
            return hero
        else:
            print("Невірний варіант")
            return None

    def __str__(self):
        effects_text = ''
        for effect in self.effects:
            effects_text += f'- {effect}\n'

        return f"{self.colored_name()} ({self.hp}/{self.max_hp} hp)\n" \
               f"attack: {self.attack} | armor: {self.armor} | magic: {self.magic}\n" \
               f"Ефекти:\n" \
               f"{effects_text}"


class Archer(Hero):
    name = 'Archer'
    hp = max_hp = 16
    attack = 5

    skill_2_name = "Град стріл"
    skill_2_description = "Лучник запускає град стріл у ворогів.\n" \
                          "Кожен ворог отримує 2-5 урону"

    def normal_attack(self, other):
        lack = random.randint(1, 100)
        if lack <= 30:
            print(f"{self.name} косий xD")
        else:
            super().normal_attack(other)

    def cast_1_skill(self, my_team, enemies_team):
        for enemy in enemies_team:
            enemy.effects.append(effects.Bleeding(enemy, 2))

    def cast_2_skill(self, my_team, enemies_team):
        print(f"{colorama.Fore.GREEN}Лучник запускає град стріл у ворогів{colorama.Fore.RESET}")
        for hero in enemies_team:
            damage = random.randint(2, 5)
            hero.get_damage(damage)
        self.did_action = True


class Slime(Hero):
    name = 'Slime'
    hp = max_hp = 30
    attack = 2
    armor = 1

    skill_1_name = 'Лікувальний слиз'
    skill_1_description = 'Слимак виділяє лікувальний слиз і лікується на половину від недостающого hp'

    skill_2_name = 'Призив міні-слимака'

    def get_damage(self, damage):
        super().get_damage(damage)
        lack = random.randint(1, 100)
        if lack > 50:
            self.regen_hp(1)

    # def cast_1_skill(self, my_team, enemies_team):
    #     self.regen_hp(my_round((self.max_hp - self.hp) / 2))
    #     self.did_action = True

    def cast_1_skill(self, my_team, enemies_team):
        self.loose_hp(10)
        self.armor += 1
        print("Армори + 1")

    def cast_2_skill(self, my_team, enemies_team):
        mini_slime = MiniSlime(self.team_number)
        my_team.append(mini_slime)
        print("Міні-слимак був призваний")
        self.loose_hp(7)
        self.did_action = True


class MiniSlime(Hero):
    name = 'MiniSlime'
    hp = max_hp = 8
    attack = 2
    armor = 1

    skill_2_name = 'Лік-слиз'

    def cast_2_skill(self, my_team, enemies_team):
        hero = self.choose_hero_from_list(my_team)
        if hero is None:
            return

        hero.regen_hp(2)
        self.did_action = True


class Assassin(Hero):
    name = 'Assassin'
    hp = max_hp = 17
    attack = 5

    skill_1_name = 'Критичний випад'
    skill_1_description = 'Ассасін робить критичний випад у вибраного ворога.\n' \
                          'Якщо це добиває ворога, Асасін отримує 5 hp.'

    def normal_attack(self, other):
        lack = random.randint(1, 100)
        if lack <= 30:
            print(f"{self.name} Робить критичний удар по {other.name}")
            other.get_damage(round(self.attack * 1.5))
        else:
            print(f"{self.name} копнув героя {other.name}")
            other.get_damage(self.attack)

    def cast_1_skill(self, my_team, enemies_team):
        hero = self.choose_hero_from_list(enemies_team, '--= Виберіть ворога =--')
        if hero is None:
            return

        print(f"{self.colored_name()} зробив критичний випад в героя {hero.colored_name()}")
        hero.get_damage(self.attack * 2)
        if not hero.alive:
            self.regen_hp(5)
        self.did_action = True


class Doctor(Hero):
    name = 'Doctor'
    hp = max_hp = 18
    attack = 2
    armor = 0

    skill_1_name = "Перекачка здоровья"
    skill_1_description = 'Доктор выбирает 1 врага, затем выбирает 1 союзника (в том числе и себя).\n' \
                          'Затем высмактывает 3-5 здоровья из выбранного врага и\n' \
                          'восстанавливает столько же выбранному союзнику.'

    def get_damage(self, damage):
        lack = random.randint(1, 100)
        if lack <= 30:
            print(f"У {self.name} влітає {0}/{damage} урона бо {self.name} ухилився")
        else:
            super().get_damage(damage)

    def cast_1_skill(self, my_team, enemies_team):
        enemy_hero = self.choose_hero_from_list(enemies_team)
        if enemy_hero is None:
            return

        teammate_hero = self.choose_hero_from_list(my_team)
        if teammate_hero is None:
            return

        hp = random.randint(3, 5)
        enemy_hero.loose_hp(hp)
        if enemy_hero.alive is False:
            hp += enemy_hero.hp
        teammate_hero.regen_hp(hp)
        self.did_action = True


class Boxer(Hero):
    name = 'Boxer'
    hp = max_hp = 25
    attack = 3
    armor = 1

    skill_1_name = "Нокаут"
    skill_1_description = 'Боксер вибирає ціль і оглушує її на 1 хід,\n' \
                          'а також наносить їй 5 урона'
    skill_2_name = 'Вогнений апперкот'
    skill_2_description = ''

    def cast_1_skill(self, my_team, enemies_team):
        target_hero = self.choose_hero_from_list(enemies_team)
        if target_hero is None:
            return

        target_hero.get_damage(5)
        target_hero.effects.append(
            effects.Stun(target_hero, 1)
        )

    def cast_2_skill(self, my_team, enemies_team):
        target_hero = self.choose_hero_from_list(enemies_team)
        if target_hero is None:
            return
        target_hero.get_damage(3)
        target_hero.effects.append(
            effects.Fire(target_hero, 3)
        )


def main():
    team1 = [Assassin(1), Doctor(1)]
    team2 = [Archer(2), Slime(2), Boxer(2)]

    round_ = 1
    while True:
        for hero in team1:
            hero.make_move_menu(team1, team2)
        for hero in team2:
            hero.make_move_menu(team2, team1)

        round_ += 1


main()
