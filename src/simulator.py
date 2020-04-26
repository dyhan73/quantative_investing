import strategies


if __name__ == "__main__":
    start_date = '20070920'
    duration_day = int(365 / 1)
    seed_money = 10000000

    loop_count = 0
    while True:
        target_date = strategies.get_target_date(start_date, days=duration_day)
        if target_date > '20200423':
            break
        loop_count = loop_count + 1
        df = strategies.get_plus_per_by_date(start_date)
        df = strategies.set_indicator_ranking(df)
        strategy_dict = strategies.get_dict_candidates_of_strategies(df)
        # rslt =strategies. get_earnings_of_date(strategy_dict['magic'], target_date, seed_money)
        rslt = strategies.get_earnings_of_date(strategy_dict['svm'], target_date, seed_money)
        # rslt = strategies.get_earnings_of_date(strategy_dict['super_values'], target_date, seed_money)

        print('start_date : ', start_date, ', target_date : ', target_date)
        print('\tbuy : ', '{:,}'.format(int(rslt['buy'].sum())))
        print('\tsell : ', '{:,}'.format(int(rslt['sell'].sum())))
        print('\tgain : ', '{:,}'.format(int(rslt['gain'].sum())))
        cagr = 100 * (rslt['sell'].sum() - rslt['buy'].sum()) / rslt['buy'].sum()
        print('\tcagr : ', '%.2f' % (100 * (rslt['sell'].sum() - rslt['buy'].sum()) / rslt['buy'].sum()))
        if cagr > 200:
            for row in rslt.iterrows():
                print(row)

        start_date = target_date
        seed_money = rslt['sell'].sum()

    cagr = pow(seed_money / 10000000, 1 / loop_count) - 1
    print('loop_cnt : ', loop_count)
    print('CAGR : %.2f' % (100 * cagr))
