import poker
import players
import strategies

print('=== program started ===\n')
t = poker.table()
a = int(input('enter player number: '))
for i in range(0, a):
	name = input('enter player{0} name: '.format(i))
	start_money = input('enter player{0} start amount of money: '.format(i))
	dbg_p = players.player(name, start_money, strategies.random_)
	t.add_player(dbg_p)
print('=== players added ===')

round_number = 1

while len(t.players) > 1:
	print('=== ROUND ' + str(round_number) + ' ===')
	t.take_new_deck()
	t.deck.shuffle()
	t.move_blinds()
	t.take_blinds()

	if len(t.players) < 2:
		break
	else:
		for p in t.players:
			p.cards.append(t.deck.pop())
			p.cards.append(t.deck.pop())
			print('DEBUG: {0}\'s cards: {1}'.format(p.name, p.cards))

		t.trade()
		t.show_flop()

		t.trade()
		t.show_turn()

		t.trade()
		t.show_river()

		t.trade()
		t.finish_round()
		round_number += 1

print(t.players[0].name + ' is the winner!')

input('press enter to exit')
