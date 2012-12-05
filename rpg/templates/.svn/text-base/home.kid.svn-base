<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
<head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
    <meta http-equiv="Pragma" content="no-cache" />
    <title>FighterMan - Home</title>
</head>

<body>
	<h1 id="title_home">Home</h1>
	<div id="feed" class="floatRight">
		<h2>Recent News:</h2>
	<!--<span py:replace="feed(news)"/> -->
	<table>
	<tr>
	<th>Time</th>
	<th>What Happened</th>
	</tr>
	<tr py:for="n in news">
		<!-- earlier than today: print all ${n.time.year}-${n.time.month}-${n.time.day}-->
		<td py:if="not n.time.date() == today" class="oldmessage">${n.time}</td>
		<!-- today: print time only-->
		<td py:if="n.time.date() == today" class="todaymessage">${n.time.time()}</td>
		<td class="${n.category}">${n.msg}</td>
	</tr>
	</table>
	</div>
	<table id="badge">
		<tr>
			<td rowspan="11"><img src="${tg.url('/static/images/fighters/' + fighter.name + '_med.png?')}" alt="${fighter.name}"/></td>
		</tr>
		<tr>
			<td colspan="2"><h2>${fighter.name}</h2></td>
		</tr>
		<tr>
			<td colspan="2"><span id='wins' title='Wins'>${fighter.wins}</span> - <span id='losses' title='Losses'>${fighter.losses}</span> - <span id='draws' title='Draws'>${fighter.draws}</span></td>
		</tr>
		<tr>
			<td>Level</td>
			<th>${fighter.level}</th>
		</tr>
		<tr>
			<td>Money</td>
			<th>$ ${tg.identity.user.money}</th>
		</tr>
		<tr>
			<td>Experience</td>
			<th>${fighter.exp}</th>
		</tr>
		<tr>
			<td>Health</td>
			<th>${fighter.hp}</th>
		</tr>
		<tr>
			<td>Strength</td>
			<th>${fighter.getStrength()}</th>
		</tr>
		<tr>
			<td>Speed</td>
			<th>${fighter.getSpeed()}</th>
		</tr>
		<tr>
			<td>Defence</td>
			<th>${fighter.getDefence()}</th>
		</tr>
		<tr>
			<td>Conditioning</td>
			<th>${fighter.getConditioning()}</th>
		</tr>

	</table>
</body>
</html>
