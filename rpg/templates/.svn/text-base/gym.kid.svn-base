<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
<head>
	<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
	<title>FighterMan - Gym</title>
	<script type="text/javascript">
		function updateImage() {
			var d = doSimpleXMLHttpRequest("${tg.url('/updateimage')}",
			{
				'body':getElement("body").value,
				'hair':getElement("hair").value,
				'mouth':getElement("mouth").value,
				'eyes':getElement("eyes").value,
				'face':getElement("face").value
			});
			d.addCallback(function (result)
			{
				getElement("fighter").src = "${tg.url('/static/images/fighters/' + fighter.name + '_med.png?')}" + new Date().getTime();
			});
		}
		
		function equipGear(num) {
			var d = loadJSONDoc("${tg.url('/equipgear')}", {'gear_id':num});
			d.addCallback(function (result)
				{
					getElement("fighter").src = "${tg.url('/static/images/fighters/' + fighter.name + '_med.png?')}" + new Date().getTime();
					var rows = map(replace, result["inventory"]);                  
				});
		}

		function replace(gear) {
			var link = getElement("e" + gear["id"]);
			if (gear["link"] == true) {
				link.innerHTML = "Equipped";
			} else {
				span = SPAN({'id':'e' + gear["id"]}, A({'href':'#', 'onclick':'equipGear(' + gear["id"] + ');'}, "Equip"));
				replaceChildNodes(link, span);
			}
		}
	
		function decrement(stat) {
			var val = parseInt(getElement(stat).value);
			if (val > 0) {
				getElement(stat).value = val-1;
				getElement("points").value = parseInt(getElement("points").value) + 1;
				updatestat(stat);
			}
	
		}
	
		function increment(stat) {
			var val = parseInt(getElement(stat).value);
			if (!(val >= 10)) {
				if (parseInt(getElement("points").value) > 0) {
				   getElement(stat).value = val+1;
				   getElement("points").value = parseInt(getElement("points").value) - 1;
				   updatestat(stat);
				}
			}
		}
		
		function updatestat(stat) {
			getElement("new_"+stat).value = parseInt(getElement("base_"+stat).value) + parseInt(getElement(stat).value);			
		}
	</script>

	<script py:if="not fighter.equipment_set" type="text/javascript">
		function updateEquipmentStat(equipment) {
			var d = doSimpleXMLHttpRequest("${tg.url('/getEquipmentStats')}", {'equipment':getElement(equipment).value});
			d.addCallback(function (result)
			{
				var myjson = result.responseText;
				var myobj = eval('(' + myjson + ')');
				getElement(equipment+"_str").value = myobj.strength;
				getElement(equipment+"_spd").value = myobj.speed;
				getElement(equipment+"_def").value = myobj.defence;
				getElement(equipment+"_con").value = myobj.conditioning;
			});
		}
	</script>
</head>

<body>
	<h1 id="title_gym">Gym</h1>
	<table class="whiteTable">
		<tr>
			<td>
				<img id="fighter" src="${tg.url('/static/images/fighters/' + fighter.name + '_med.png')}" alt="${fighter.name}"/>
			</td>
			<td>
				<div class="tabber">
					<div class="tabbertab" title="Locker">
						<table border="1" id="mygear">
							<tr>
								<th>Name</th>
								<th>Type</th>
								<th>Level</th>
								<th>Strength</th>
								<th>Speed</th>
								<th>Defence</th>
								<th>Conditioning</th>
							</tr>
							<tr py:for="gear in inventory" py:attrs="{'class': (gear.level > fighter.level and 'levelTooHigh')}">
								<td py:content="gear.name"/>
								<td py:content="gear.type"/>
								<td py:content="gear.level"/>
								<td py:content="gear.strength"/>
								<td py:content="gear.speed"/>
								<td py:content="gear.defence"/>
								<td py:content="gear.conditioning"/>
								<td py:if="(not gear == fighter.trunks) and (not gear == fighter.boots) and (not gear == fighter.gloves) and (not gear.level > fighter.level)"><span id="e${gear.id}"><a href="#" onclick="javascript:equipGear(${gear.id});">Equip</a></span></td>
								<td py:if="(gear == fighter.trunks) or (gear == fighter.boots) or (gear == fighter.gloves)"><span id="e${gear.id}">Equipped</span></td>
							</tr>
						</table>
						<p>Select the gear you would like your fighter to wear during fights. To purchase more gear please visit the <a href="${tg.url('./shop')}">shop</a>.</p>
					</div>
					<div class="tabbertab" title="Plastic Surgery">
						<table>
							<tr>
							<th>Body:</th>
							<td>
									<select name="body" id="body" onchange="javascript:updateImage();">
										<option py:for="body in bodies" py:content="body.name" py:attrs="dict(value=body.name, selected=(fighter.body.name == body.name and 'selected' or None))"/>
									</select>
								</td>
							</tr>
							<tr>
								<th>Eyes:</th>
								<td>
									<select name="eyes" id="eyes" onchange="javascript:updateImage();">
										<option py:for="eye in eyes" py:content="eye.name" py:attrs="dict(value=eye.name, selected=(fighter.eyes.name == eye.name and 'selected' or None))"/>
									</select>
								</td>
							</tr>
							<tr>
								<th>Hair:</th>
								<td>
									<select name="hair" id="hair" onchange="javascript:updateImage();">
										<option py:for="h in hair" py:content="h.name" py:attrs="dict(value=h.name, selected=(fighter.hair.name == h.name and 'selected' or None))"/>
									</select>
								</td>
							</tr>
							<tr>
								<th>Mouth:</th>
								<td>
									<select name="mouth" id="mouth" onchange="javascript:updateImage();">
										<option py:for="mouth in mouths" py:content="mouth.name" py:attrs="dict(value=mouth.name, selected=(fighter.mouth.name == mouth.name and 'selected' or None))"/>
									</select>
								</td>
							</tr>
							<tr>
								<th>Face:</th>
								<td>
									<select name="face" id="face" onchange="javascript:updateImage();">
										<option py:for="face in faces" py:content="face.name" py:attrs="dict(value=face.name, selected=(fighter.face.name == face.name and 'selected' or None))"/>
									</select>
								</td>
							</tr>
						</table>
					</div>
					<div class="tabbertab" title="Equipment">
						<table>
							<tr>
								<th>Equipment</th>
								<th>Level</th>
								<th>Strength</th>
								<th>Speed</th>
								<th>Defence</th>
								<th>Conditioning</th>
								<th>Using</th>
							</tr>
							<tr py:for="e in equipment" py:if="e.type == 'Gym'">
								<td py:content="e.name" py:attrs="dict(id=(e.level > fighter.level and 'levelTooHigh' or None))"/>
								<td align="center" py:content="e.level"/>
								<td align="center" py:content="e.strength"/>
								<td align="center" py:content="e.speed"/>
								<td align="center" py:content="e.defence"/>
								<td align="center" py:content="e.conditioning"/>
								<td align="center" py:if="e.name == fighter.equipment1.name or e.name == fighter.equipment2.name or e.name == fighter.equipment3.name">yes</td>
								<td align="center" py:if="not(e.name == fighter.equipment1.name or e.name == fighter.equipment2.name or e.name == fighter.equipment3.name)">no</td>
							</tr>
							</table>
							<p py:if="not fighter.equipment_set">Select the equipment you would like to use for today's training. To purchase more equipment please visit the <a href="${tg.url('./shop')}">shop</a>.</p>
							<p py:if="fighter.equipment_set">You have selected the following equipment to be used for the day. Please check back tomorrow if you would like to change the equipment you are using.</p>
							<form action="setTrainingEquipment">
							<table>
							<tr>
								<th>Equipment</th>
								<th>Strength</th>
								<th>Speed</th>
								<th>Defence</th>
								<th>Conditioning</th>
							</tr>
							
							<tr py:if="not fighter.equipment_set">
								<td>
									<select name="equipment1" id="e_1" onchange="updateEquipmentStat('e_1')" onkeyup="updateEquipmentStat('e_1')">
										<option py:for="item in equipment" py:if="not item.level > fighter.level" py:content="item.name" py:attrs="dict(value=item.name, selected=(fighter.equipment1.name == item.name or None))"/>
									</select>
								</td>
								<td align="center"><input class="noBorder" type="text" id="e_1_str" name="strength" value ="${fighter.equipment1.strength}" size="2" readonly="readonly "/></td>
								<td align="center"><input class="noBorder" type="text" id="e_1_spd" name="speed" value ="${fighter.equipment1.speed}" size="2" readonly="readonly "/></td>
								<td align="center"><input class="noBorder" type="text" id="e_1_def" name="defence" value ="${fighter.equipment1.defence}" size="2" readonly="readonly "/></td>
								<td align="center"><input class="noBorder" type="text" id="e_1_con" name="conditioning" value ="${fighter.equipment1.conditioning}" size="2" readonly="readonly "/></td>
							</tr>
							<tr py:if="not fighter.equipment_set">
								<td>
									<select name="equipment2" id="e_2" onchange="updateEquipmentStat('e_2')" onkeyup="updateEquipmentStat('e_2')">
										<option py:for="item in equipment" py:if="not item.level > fighter.level" py:content="item.name" py:attrs="dict(value=item.name, selected=(fighter.equipment2.name == item.name or None))"/>
									</select>
								</td>
								<td align="center"><input class="noBorder" type="text" id="e_2_str" name="strength" value ="${fighter.equipment2.strength}" size="2" readonly="readonly "/></td>
								<td align="center"><input class="noBorder" type="text" id="e_2_spd" name="speed" value ="${fighter.equipment2.speed}" size="2" readonly="readonly "/></td>
								<td align="center"><input class="noBorder" type="text" id="e_2_def" name="defence" value ="${fighter.equipment2.defence}" size="2" readonly="readonly "/></td>
								<td align="center"><input class="noBorder" type="text" id="e_2_con" name="conditioning" value ="${fighter.equipment2.conditioning}" size="2" readonly="readonly "/></td>
							</tr>
							<tr py:if="not fighter.equipment_set">
								<td>
									<select name="equipment3" id="e_3" onchange="updateEquipmentStat('e_3')" onkeyup="updateEquipmentStat('e_3')">
										<option py:for="item in equipment" py:if="not item.level > fighter.level" py:content="item.name" py:attrs="dict(value=item.name, selected=(fighter.equipment3.name == item.name or None))"/>
									</select>
								</td>
								<td align="center"><input class="noBorder" type="text" id="e_3_str" name="strength" value ="${fighter.equipment3.strength}" size="2" readonly="readonly "/></td>
								<td align="center"><input class="noBorder" type="text" id="e_3_spd" name="speed" value ="${fighter.equipment3.speed}" size="2" readonly="readonly "/></td>
								<td align="center"><input class="noBorder" type="text" id="e_3_def" name="defence" value ="${fighter.equipment3.defence}" size="2" readonly="readonly "/></td>
								<td align="center"><input class="noBorder" type="text" id="e_3_con" name="conditioning" value ="${fighter.equipment3.conditioning}" size="2" readonly="readonly "/></td>
							</tr>
							<tr py:if="not fighter.equipment_set">
								<td colspan="5" align="right"><input type="submit" value="Use Equipment"/></td>
							</tr>
							
							<tr py:if="fighter.equipment_set">
								<td>${fighter.equipment1.name}</td>
								<td align="center">${fighter.equipment1.strength}</td>
								<td align="center">${fighter.equipment1.speed}</td>
								<td align="center">${fighter.equipment1.defence}</td>
								<td align="center">${fighter.equipment1.conditioning}</td>
							</tr>
							<tr py:if="fighter.equipment_set">
								<td>${fighter.equipment2.name}</td>
								<td align="center">${fighter.equipment2.strength}</td>
								<td align="center">${fighter.equipment2.speed}</td>
								<td align="center">${fighter.equipment2.defence}</td>
								<td align="center">${fighter.equipment2.conditioning}</td>
							</tr>
							<tr py:if="fighter.equipment_set">
								<td>${fighter.equipment3.name}</td>
								<td align="center">${fighter.equipment3.strength}</td>
								<td align="center">${fighter.equipment3.speed}</td>
								<td align="center">${fighter.equipment3.defence}</td>
								<td align="center">${fighter.equipment3.conditioning}</td>
							</tr>
							</table>
							</form>
						</div>
					<div class="tabbertab" title="Trainer">
						<table py:if="not fighter.trainer == None">
							<tr>
								<th>Name</th>
								<th>Level</th>
								<th>Hire Fee</th>
								<th>Salary</th>
								<th>Points</th>
							</tr>
							<tr>
								<td py:content="fighter.trainer.name"/>
								<td py:content="fighter.trainer.level"/>
								<td py:content="fighter.trainer.hirefee"/>
								<td py:content="fighter.trainer.salary"/>
								<td py:content="fighter.trainer.points"/>
							</tr>
						</table>
						<p py:if="fighter.trainer == None">
							You currently do not have a trainer.
							To hire a trainer please visit the <a href="${tg.url('./shop')}">shop</a>.
							Trainers allow you to manually distribute a fixed amount of stat points.
						</p>
						<p py:if="not fighter.trainer == None">
							You can distribute stat points provided by your trainer.
							To hire a different trainer please visit the <a href="${tg.url('./shop')}">shop</a>.
							You can also <a href="${std.url('/firetrainer', nextpage='./gym')}">fire</a> your trainer.
						</p>
						<form action = "${tg.url('./train')}" method = "POST" py:if="not fighter.trainer == None">
						<table>		
							<tr>
								<td><input type="text" id="points" name="points" value ="${fighter.trainer_points}" size="3" readonly="readonly "/></td>
								<td colspan="2">Points Remaining</td>
							</tr>
							<tr>
								<td>Strength</td>
								<td>
									<input type="hidden" id="base_strength" name="base_strength" value ="${fighter.getStrength()-fighter.trainer_strength}"/>
									<input class="noBorder" type="text" id="new_strength" name="new_strength" value ="${fighter.getStrength()}" size="2" readonly="readonly "/>
								</td>
								<td>
								<input type="button" name="minus" value="-" onclick="decrement('strength')"/>
								<input type="text" id="strength" name="strength" value ="${fighter.trainer_strength}" size="2" readonly="readonly "/>
								<input type="button" name="plus" value="+" onclick="increment('strength')"/>
								</td>
							</tr>
							<tr>
								<td>Speed</td>
								<td>
									<input type="hidden" id="base_speed" name="base_speed" value ="${fighter.getSpeed()-fighter.trainer_speed}"/>
									<input class="noBorder" type="text" id="new_speed" name="new_speed" value ="${fighter.getSpeed()}" size="2" readonly="readonly "/>
								</td>
								<td>
								<input type="button" name="minus" value="-" onclick="decrement('speed')"/>
								<input type="text" id="speed" name="speed" value ="${fighter.trainer_speed}" size="2" readonly="readonly "/>
								<input type="button" name="plus" value="+" onclick="increment('speed')"/>
								</td>
							</tr>
							<tr>
								<td>Defence</td>
								<td>
									<input type="hidden" id="base_defence" name="base_defence" value ="${fighter.getDefence()-fighter.trainer_defence}"/>
									<input class="noBorder" type="text" id="new_defence" name="new_defence" value ="${fighter.getDefence()}" size="2" readonly="readonly "/>
								</td>
								<td>
								<input type="button" name="minus" value="-" onclick="decrement('defence')"/>
								<input type="text" id="defence" name="defence" value ="${fighter.trainer_defence}" size="2" readonly="readonly "/>
								<input type="button" name="plus" value="+" onclick="increment('defence')"/>
								</td>
							</tr>
							<tr>
								<td>Conditioning</td>
								<td>
									<input type="hidden" id="base_conditioning" name="base_conditioning" value ="${fighter.getConditioning()-fighter.trainer_conditioning}"/>
									<input class="noBorder" type="text" id="new_conditioning" name="new_conditioning" value ="${fighter.getConditioning()}" size="2" readonly="readonly "/>
								</td>
								<td>
								<input type="button" name="minus" value="-" onclick="decrement('conditioning')"/>
								<input type="text" id="conditioning" name="conditioning" value ="${fighter.trainer_conditioning}" size="2" readonly="readonly "/>
								<input type="button" name="plus" value="+" onclick="increment('conditioning')"/>
								</td>
							</tr>
							<tr>
								<td colspan="2" align="right"><input type="submit" value="Train"/></td>
							</tr>
						</table>
						</form>
					</div>
				</div>
			</td>
		</tr>
	</table>
</body>
</html>
