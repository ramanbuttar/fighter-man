<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
<head>
	<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
	<title>FighterMan - Fight Results</title>
</head>
<body>
	<h1 id="title_arena">Fight Results</h1>
	<h1>Fight Results</h1>	
	<br />
	<table id="card" py:if="result != 2">
		<tr>
			<th colspan="14">Scorecard</th>
		</tr>
		<tr>
			<th>Fighters</th>
			<th py:for="i in range(1,13)" py:content="i"/>
			<th>Total</th>
		</tr>
		<tr>
			<td>${player}</td>
			<td py:for="score in scorecard">
				<span py:if="score == 1">10</span>
				<span py:if="score == -1">9</span>
				<span py:if="score == 0">9</span>
				<span py:if="score == 2">KO</span>
				<span py:if="score == '-' or score == -2">-</span>
			</td>
			<td py:if="scorecard[-1] != '-'" py:content="(scorecard.count(1)*10)+(scorecard.count(-1)*9)"/>
			<td py:if="scorecard[-1] == '-'">-</td>
		</tr>
		<tr>
			<td>${opponent}</td>
			<td py:for="score in scorecard">
				<span py:if="score == -1">10</span>
				<span py:if="score == 1">9</span>
				<span py:if="score == 0">9</span>
				<span py:if="score == -2">KO</span>
				<span py:if="score == '-' or score == 2">-</span>
			</td>
			<td py:if="scorecard[-1] != '-'" py:content="(scorecard.count(-1)*10)+(scorecard.count(1)*9)"/>
			<td py:if="scorecard[-1] == '-'">-</td>
		</tr>
		<tr>
			<th colspan="14">
				<p py:if="result == 1 and scorecard[-1] == '-'">Your fighter won by knockout in round ${scorecard.index(2) + 1}! Gained ${expgain} experience and $ ${winnings}.</p>
				<p py:if="result == 1 and scorecard[-1] != '-'">Your fighter won by decision after 12 rounds! Gained ${expgain} experience and $ ${winnings}.</p>
				<p py:if="result == 0">The fight was a draw!</p>
				<p py:if="result == -1 and scorecard[-1] != '-'">Your fighter lost by decision after 12 rounds.</p>
				<p py:if="result == -1 and scorecard[-1] == '-'">Your fighter lost by knockout in round ${scorecard.index(-2) + 1}.</p>	

				<p py:if="result == 2">You can't fight that opponent...</p>
			</th>
		</tr>
	</table>
	<a id="fightagain" class="floatRight" href="${std.url('/arena', opp=opponent)}">Fight Again?</a>
</body>
</html>
