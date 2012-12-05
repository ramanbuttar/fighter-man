<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
<head>
	<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
	<title>FighterMan - Auction</title>
	<script type = "text/javascript">
		function minBid(bid) {
		    document.getElementById("bid").value = parseInt(bid)+25;
		}

		function checkAuction() {    
		    check = false;
		    radios = document.getElementsByName("auctionID");
	        for(i=0; radios.length > i; i++) {        
		        if(radios[i].checked == true) {
		            check = true;
		            document.bidForm.submit();
	    	        return;
		        }
		    }
	    	alert("You must select an item to bid on before you can place a bid.");
		}

	</script>
</head>

<body>
	<h1 id="title_auction">Auctions</h1>
	<h2 class="money" >Money in the Bank: $ ${tg.identity.user.money}</h2>
	<div class = "tabber">
	    <div class="tabbertab" title="Auctions">
			<form action="${tg.url('/auction')}" method="get">
				Show:
				<select name="filter" onchange="this.form.submit()">
					<option value="None" selected="selected"/>
					<option value="All">All</option>
					<option value="Gloves">Gloves</option>
					<option value="Boots">Boots</option>
					<option value="Trunks">Trunks</option>
				</select>
			</form>
			<form action="placebid" method="post" name="bidForm">
			Bid Amount:
				<input type="text" id="bid" name="bid"/>        
				<input type="button" value = "Place Bid" onclick="checkAuction()"/>
				<div py:replace="auctiongrid(auctions)"/>
			</form>    	    
        	<p py:if="auctioncount == 0">No Auctions</p>
	    </div>
	    <div class="tabbertab" title="My Bids">
    	    <div py:replace="viewgrid(mybids)"/>
    	    <p py:if="mybids.count() == 0">No Auctions</p>
		</div>
	    <div class="tabbertab" title="My Auctions">  
	        <p>Warning: Cancelling an auction will incur a fee of 5% of the item's in shop value</p> 
			<form action="createauction" method="post">
			<table id="myauctions">
				<tr>
					<td>
						Item:
						<select name="auctionitem" id="auctionitem">
							<option py:for="item in inventory" py:content="item.name"/>
						</select>
					</td>
					<td>
						Starting Bid:
						<input type="text" id="startbid" name="startbid"/>
					</td>
					<td>
						Auction Length(days):
						<select name="auctionlength" id = "auctionlength">
							<option py:for="i in range(1,8)" py:content="i"/>
						</select>
					</td>
					<td>
						<input type="submit" value="Create Auction"/>
					</td>
				</tr>
			</table>
			</form>
        	<div py:replace="owngrid(myauctions)"/>
        	<p py:if="myauctions.count() == 0">No Auctions</p> 
    	</div>
	</div>
</body>
</html>
