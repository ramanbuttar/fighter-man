<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
<head>
	<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
	<title>FighterMan - Arena</title>
</head>
<body>
	<h1 id="title_arena">Find Opponent</h1>
	<h2 class="money" >Money in the Bank: $ ${tg.identity.user.money}</h2>
	<p>Click on fighter's name from the list below to challenge to a fight:</p>
	<div py:replace="grid(fighters)"/>
		<table py:if="opponent != None" id="taleoftape">
			<tr>
				<th colspan="5">Tale of the Tape</th>
			</tr>
			<tr>
				<td rowspan="11"><img src = "${tg.url('/static/images/fighters/' + me.name + '_med.png')}" alt="${me.name}"/></td>
				<td></td>
				<td></td>
				<td></td>
				<td rowspan="11"><img src = "${tg.url('/static/images/fighters/' + opponent.name + '_med.png')}" alt="${opponent.name}"/></td>
			</tr>
			<tr>
				<th>${me.name}</th>
				<th>vs.</th>
				<th>${opponent.name}</th>
			</tr>
			<tr>
				<td>${me.wins} - ${me.losses} - ${me.draws}</td>
				<th>win/loss</th>
				<td>${opponent.wins} - ${opponent.losses} - ${opponent.draws}</td>
			</tr>
			<tr>
				<td>${me.level}</td>
				<th>level</th>
				<td>${opponent.level}</td>
			</tr>
			<tr>
				<td>${me.exp}</td>
				<th>exp</th>
				<td>${opponent.exp}</td>
			</tr>
			<tr>
				<td>${me.getHP()}</td>
				<th>hp</th>
				<td>${opponent.getHP()}</td>
			</tr>
			<tr>
				<td>${me.getStrength()}</td>
				<th>strength</th>
				<td>${opponent.getStrength()}</td>
			</tr>
			<tr>
				<td>${me.getSpeed()}</td>
				<th>speed</th>
				<td>${opponent.getSpeed()}</td>
			</tr>
			<tr>
				<td>${me.getDefence()}</td>
				<th>defence</th>
				<td>${opponent.getDefence()}</td>
			</tr>
			<tr>
				<td>${me.getConditioning()}</td>
				<th>conditioning</th>
				<td>${opponent.getConditioning()}</td>
			</tr>
			<tr>
				<th colspan="3" py:if="(opponent != None) and (me.id != opponent.id)">
					<a py:if="me.level - opponent.level > 3 or not(me.level-opponent.level > 3)" href="${std.url('/rumble', opponent_id = opponent.id)}">FIGHT</a>
					</th>
			</tr>
		</table>	
	
</body>
</html>
