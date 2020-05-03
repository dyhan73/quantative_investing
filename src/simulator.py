import strategies


def rebalance_once(start, end, days, seed=10000000, method='magic'):
    """
    주기에 따라 전체 리밸런싱 하는 방식 (마법공식, 슈퍼가치전략 등이 해당)
    :param start:
    :param end:
    :param days:
    :param seed:
    :param method: string ('magic', 'svm', 'super_values')
    :return:
    """
    start_date = start
    seed_money = seed

    loop_count = 0
    while True:
        target_date = strategies.get_target_date(start_date, days=days)
        if target_date > end:
            break
        loop_count = loop_count + 1
        df = strategies.get_plus_per_by_date(start_date)
        df = strategies.set_indicator_ranking(df)
        strategy_dict = strategies.get_dict_candidates_of_strategies(df)
        rslt = strategies.get_earnings_of_date(strategy_dict[method], target_date, seed_money)

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


def rebalance_interval(start, end, duration_days=365, interval_days=30, seed=10000000, method='svm'):
    start_date = start
    seed_money = seed

    end_date = strategies.get_target_date(start_date, days=duration_days)

    loop_count = 0
    while True:
        target_date = strategies.get_target_date(start_date, days=interval_days)
        if target_date > end_date:
            break
        loop_count = loop_count + 1
        df = strategies.get_plus_per_by_date(start_date)
        df = strategies.set_indicator_ranking(df)
        strategy_dict = strategies.get_dict_candidates_of_strategies(df)
        rslt = strategies.get_earnings_of_date(strategy_dict[method], target_date, seed_money)

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


if __name__ == "__main__":
    rebalance_once('20070710', '20200423', int(365 / 1), 10000000, 'svm')

