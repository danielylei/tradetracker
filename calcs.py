def totals (c):
    #check for empty list 
    if len(c)> 0:
        #c is list of executions
        totalgainloss = 0.00
        totalgained = 0.00
        totallost = 0.00

        numwinningtrades = 0
        averagewinningtrade = 0.00
        numlosingtrades = 0
        averagelosingtrade = 0.00
        winratio = 0.00
        lossratio = 0.00

        largestwin = 0.00
        largestloss = 0.00

        numtrades = 0
        totalshares = 0
        avgshares = 0
        persharegain = 0.00
        avgtradegain = 0.00
        profitfactor = 0.00

        totalcommissions = 0.00
        totalfees = 0.00

        numdays = 0
        dailygainloss = 0.00
        dailyshares = 0



        for trade in c:
            #for e in trade.execution_set.all():
            #cashflow = e.amount
            cashflow = trade.pnl
            if cashflow > 0:
                if cashflow > largestwin:
                    largestwin = cashflow
                    largestwintrade = trade

                totalgained += cashflow
                numwinningtrades += 1
            else:
                if cashflow < largestloss:
                    largestloss = cashflow
                    largestlosstrade = trade
                totallost += cashflow
                numlosingtrades += 1

            #totalshares += e.quantity
            #totalcommissions += e.commission
            #totalfees += e.fees
            totalshares += trade.volume
            totalcommissions += 0
            totalfees += 0

        totalgainloss = totalgained + totallost

        numtrades = numwinningtrades + numlosingtrades
        if numwinningtrades == 0:
            averagewinningtrade = 0
        else:
            averagewinningtrade = totalgained/numwinningtrades
        
        if numlosingtrades == 0:
            averagelosingtrade = 0
        else:
            averagelosingtrade = totallost/numlosingtrades
        avgshares = totalshares//numtrades

        if totalshares == 0:
            persharegain = totalgainloss
        else:
            persharegain = totalgainloss/totalshares

        avgtradegain = totalgainloss/numtrades

        if totallost == 0:
            #idk if math is right
            profitfactor = totalgained
        else:
            profitfactor = -1*totalgained/totallost
        winratio = numwinningtrades/numtrades
        lossratio = numlosingtrades/numtrades
        #wrong we want to find the number of unique dates with trades.
        delta = c.last().date - c.first().date 
        numdays = delta.days + 1
        print(numdays)

        if numdays != 0:
            dailygainloss = totalgainloss / numdays

        #print these values
        totalgainloss = str(round(totalgainloss,2))
        dailygainloss = str(round(dailygainloss,2))
        if numdays == 0:
            dailyshares = 0
        else:
            dailyshares = str(totalshares//numdays)
        numdays = str(numdays)
        averagewinningtrade = str(round(averagewinningtrade,2))
        averagelosingtrade = str(round(averagelosingtrade,2))
        largestwin = str(round(largestwin,2))
        #largestwintrade, should be hyperlink to details of largest winning trade
        largestloss = str(round(largestloss,2))
        #largestlosstrade, should be hyperlink to details of largest losing trade
        avgshares = str(avgshares)
        persharegain = str(round(persharegain,2))
        avgtradegain = str(round(avgtradegain,2))
        totalgained = str(round(totalgained,2))
        totallost = str(round(totallost,2))
        profitfactor = str(round(profitfactor,2))
        numtrades = str(numtrades)
        numwinningtrades = str(numwinningtrades)
        winratio = str(round(winratio,3)*100)+'%'
        numlosingtrades = str(numlosingtrades)
        lossratio = str(round(lossratio,3)*100)+'%'
        totalshares = str(totalshares)
        totalcommissions = str(round(totalcommissions,2))
        totalfees = str(round(totalfees,2))


        return {'total_gain_loss': totalgainloss,
                'daily_gain_loss': dailygainloss,
                'daily_shares': dailyshares,
                'numdays': numdays,
                'average_winning_trade': averagewinningtrade,
                'average_losing_trade': averagelosingtrade,
                'largest_win': largestwin,
                'largest_loss': largestloss,
                'avg_shares': avgshares,
                'per_share_gain':persharegain,
                'avg_trade_gain': avgtradegain,
                'total_gained': totalgained,
                'total_lost': totallost,
                'profit_factor': profitfactor,
                'num_trades': numtrades,
                'num_winning_trades': numwinningtrades,
                'win_ratio': winratio,
                'num_losing_trades': numlosingtrades,
                'loss_ratio': lossratio,
                'total_shares': totalshares,
                'total_commissions': totalcommissions,
                'total_fees': totalfees,
        }
