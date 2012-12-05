<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
<head>
	<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
	<title>FighterMan - Shop</title>
	<script type="text/javascript">
		function updateImage(file) {
			getElement("preview").src="${tg.url('/static/images/equipment/')}" + file;
			getElement("preview").alt=file;
		}
		function clearImage() {
			getElement("preview").src="";
			getElement("preview").alt="";
		}
	</script>

</head>
<body>
	<h1 id="title_shop">Shop</h1>
	<h2 class="money" >Money in the Bank: $ ${tg.identity.user.money}</h2>
	<div id="shopdiv">
		<h2>Preview:</h2>
		<img id="preview" src="${tg.url('/static/images/pixel.png')}" alt="No Preview"/>
	</div>
	<div class="tabber" id="shop">
		<div class="tabbertab" title="Gear">
			<form action="${tg.url('/shop')}" method="get">
				Show:
				<select name="filter" onchange="this.form.submit()">
					<option value="None" selected="selected"/>
					<option value="All">All</option>
					<option value="Gloves">Gloves</option>
					<option value="Boots">Boots</option>
					<option value="Trunks">Trunks</option>
				</select>
			</form>
			<table border="1">
				<tr>
					<th>Name</th>
					<th>Type</th>
					<th>Level</th>
					<th>Strength</th>
					<th>Speed</th>
					<th>Defence</th>
					<th>Conditioning</th>
					<th>Cost</th>
				</tr>
				<tr py:for="gear in equipment" onmouseout="javascript:clearImage();" onmouseover="javascript:updateImage('${gear.filename[gear.filename.rfind('/')+1:]}');" py:attrs="{'class' : (gear.cost > tg.identity.user.money and 'costTooHigh')}">
					<td py:content="gear.name"/>
					<td py:content="gear.type"/>
					<td py:content="gear.level" py:attrs="{'class' : (gear.level > fighter.level and 'levelTooHigh')}"/>
					<td py:content="gear.strength"/>
					<td py:content="gear.speed"/>
					<td py:content="gear.defence"/>
					<td py:content="gear.conditioning"/>
					<td py:content="gear.cost"/>
					<td py:if="not gear in inventory"><a href="${std.url('/buygear', gear_id=gear.id)}">Buy</a></td>
					<td py:if="gear in inventory">Owned</td>
				</tr>
			</table>
		</div>
		<div class="tabbertab" title="Trainers">
			<table border="1">
				<tr>
					<th>Name</th>
					<th>Level</th>
					<th>Hire Fee</th>
					<th>Salary</th>
					<th>Points</th>
				</tr>
				<tr py:for="t in trainers" py:attrs="{'class' : (t.hirefee > tg.identity.user.money and 'costTooHigh')}">
					<td py:content="t.name"/>
					<td py:content="t.level" py:attrs="{'class' : (t.level > fighter.level and 'levelTooHigh')}"/>
					<td py:content="t.hirefee"/>
					<td py:content="t.salary"/>
					<td py:content="t.points"/>
					<td py:if="not t== fighter.trainer"><a href="${std.url('/hiretrainer', trainer_id=t.id)}">Hire</a></td>
					<td color="red" py:if="t== fighter.trainer"><a href="${tg.url('/firetrainer')}">Fire</a></td>
				</tr>
			</table>
			<p py:if="tg.identity.user.fighter.trainer != None">Note: <em>hiring a new trainer will result in firing your current trainer.</em></p>
		</div>
		<div class="tabbertab" title="Equipment">
			<table border="1">
				<tr>
					<th>Name</th>
					<th>Level</th>
					<th>Strength</th>
					<th>Speed</th>
					<th>Defence</th>
					<th>Conditioning</th>
					<th>Cost</th>
				</tr>
				<tr py:for="equip in gym" py:attrs="{'class' : (equip.cost > tg.identity.user.money and 'costTooHigh')}">
					<td py:content="equip.name"/>
					<td py:content="equip.level" py:attrs="{'class' : (equip.level > fighter.level and 'levelTooHigh')}"/>
					<td py:content="equip.strength"/>
					<td py:content="equip.speed"/>
					<td py:content="equip.defence"/>
					<td py:content="equip.conditioning"/>
					<td py:content="equip.cost"/>
					<td py:if="not equip in inventory"><a href="${std.url('/buygear', gear_id=equip.id)}">Buy</a></td>
					<td py:if="equip in inventory">Owned</td>
				</tr>
			</table>
		</div>
		<div class="tabbertab" title="Sell">
			<table border="1">
				<tr>
					<th>Name</th>
					<th>Type</th>
					<th>Level</th>
					<th>Strength</th>
					<th>Speed</th>
					<th>Defence</th>
					<th>Conditioning</th>
					<th>Value</th>
				</tr>
				<tr py:for="gear in inventory" onmouseout="javascript:clearImage();" onmouseover="javascript:updateImage('${gear.filename[gear.filename.rfind('/')+1:]}');">
					<td py:content="gear.name"/>
					<td py:content="gear.type"/>
					<td py:content="gear.level"/>
					<td py:content="gear.strength"/>
					<td py:content="gear.speed"/>
					<td py:content="gear.defence"/>
					<td py:content="gear.conditioning"/>
					<td py:content="gear.cost/3"/>
					<td py:if="(not gear== fighter.trunks) and (not gear== fighter.boots) and (not gear== fighter.gloves) and (not gear== fighter.equipment1) and (not gear== fighter.equipment2) and (not gear== fighter.equipment3)"><a href="${std.url('/sellgear', gear_id=gear.id)}">Sell</a></td>
					<td py:if="(gear== fighter.trunks) or (gear== fighter.boots) or (gear== fighter.gloves)">Equipped</td>
					<td py:if="(gear== fighter.equipment1) or (gear== fighter.equipment2) or (gear== fighter.equipment3)">In Use</td>
				</tr>
			</table>
		</div>
	</div>
</body>
</html>
