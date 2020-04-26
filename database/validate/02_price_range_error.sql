select code, count(*)
from prices
where max(ifnull(close, 0), ifnull(adj_close, 0)) < low or max(ifnull(close, 0), ifnull(adj_close, 0)) > high
    and market_cap is not null
group by code
order by code;

select *
from prices
where (max(ifnull(close, 0), ifnull(adj_close, 0)) < low or max(ifnull(close, 0), ifnull(adj_close, 0)) > high)
    and market_cap is not null
    and sdate = '20100930'
;
