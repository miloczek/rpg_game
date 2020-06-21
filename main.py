from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item

#Create Witcher Signs
igni = Spell("Igni", 20, 200, "sign")
aard = Spell("Aard", 8, 100, "sign")
yrden = Spell("Yrden", 12, 110, "sign")
queen = Spell("Queen", 15, 160, "sign")
aksji = Spell("Aksji", 14, 140, "sign")

#Create Wizard Magic Spells
cure = Spell("Cure", 12, 120, "magic spell")
vitality = Spell("Vitality", 18, 200, "magic spell")


#Create some items
swallow = Item("Swallow", "potion", "Heals 50 HP", 50)
enhanced_swallow = Item("Enhanced Swallow", "potion", "Heals 100 HP", 100)
superior_swallow = Item("Superior Swallow", "potion", "Heals 500 HP", 500)
thunderbolt = Item("Thunderbolt", "elixir", "Fully restores HP/MP of one character", 9999)
full_moon = Item("Full Moon", "elixir", "Fully restores HP/MP of all characters in team", 9999)

dancing_star = Item("Dancing Star", "attack", "Deals 500 damage", 500)


player_magic = [igni, aard, yrden, cure, vitality]
player_items = [{"item": swallow, "quantity": 15}, {"item": enhanced_swallow, "quantity": 5},
                {"item": superior_swallow, "quantity": 5}, {"item":thunderbolt, "quantity": 5},
                {"item": full_moon, "quantity": 2}, {"item":dancing_star, "quantity": 5}]

#Characters
player = Person(460, 65, 60, 34, player_magic, player_items)
enemy = Person(1200, 65, 45, 25, [], [])

running = True

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("================================")
    player.choose_action()
    choice = input("Choose action:")
    index = int(choice) - 1

    if index == 0:
        dmg = player.generate_damage()
        enemy.take_damage(dmg)
        print("You attacked for", dmg, "points of damage.")
    elif index == 1:
        player.choose_magic()
        print("    0. Back to main menu")
        magic_choice = int(input("Choose magic:")) - 1

        if magic_choice == -1:
            continue

        spell = player.magic[magic_choice]
        magic_dmg = spell.generate_damage()

        current_mp = player.get_mp()

        if spell.cost > current_mp:
            print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
            continue

        player.reduce_mp(spell.cost)

        if spell.type == "magic spell":
            player.heal(magic_dmg)
            print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP." + bcolors.ENDC)
        elif spell.type == "sign":
            enemy.take_damage(magic_dmg)
            print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage" + bcolors.ENDC)

    elif index == 2:
        player.choose_item()
        print("    0. Back to main menu")
        item_choice = int(input("Choose item: ")) - 1

        if item_choice == -1:
            continue

        item = player.items[item_choice]["item"]
        if player.items[item_choice]["quantity"] == 0:
            print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
            continue
        player.items[item_choice]["quantity"] -= 1


        if item.type == "potion":
            player.heal(item.prop)
            print(bcolors.OKGREEN + "\n" + item.name + " heals for " + str(item.prop) + " HP"  + bcolors.ENDC)
        elif item.type == "elixir":
            player.hp = player.maxhp
            player.mp = player.maxmp
            print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + bcolors.ENDC)
        elif item.type == "attack":
            enemy.take_damage(item.prop)
            print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop), "points of damage" + bcolors.ENDC)

    enemy_choice = 1

    enemy_dmg = enemy.generate_damage()
    player.take_damage(enemy_dmg)
    print("Enemy attacks for", enemy_dmg)

    print("-------------------------------------")
    print("Enemy HP:", bcolors.FAIL + str(enemy.get_hp()) + "/" + str(enemy.get_max_hp()) + bcolors.ENDC + "\n")

    print("Your HP:", bcolors.OKGREEN + str(player.get_hp()) + "/" + str(player.get_max_hp()) + bcolors.ENDC + "\n")
    print("Your MP:",  bcolors.OKBLUE + str(player.get_mp()) + "/" + str(player.get_max_mp()) + bcolors.ENDC + "\n")

    if enemy.get_hp() == 0:
        print(bcolors.OKGREEN + "You win" + bcolors.ENDC)
        running = False
    elif player.get_hp() == 0:
        print(bcolors.FAIL + "Enemy has defeated yoy!" + bcolors.ENDC)
        running = False