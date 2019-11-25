-------------------------------------------------------
--Normal/Gaussian Distribution sampler
--Credits: https://rosettacode.org/wiki/Statistics/Normal_distribution
function gaussian (mean, variance)
    return  math.sqrt(-2 * variance * math.log(math.random())) *
            math.cos(2 * math.pi * math.random()) + mean
end
 
function mean (t)
    local sum = 0
    for k, v in pairs(t) do
        sum = sum + v
    end
    return sum / #t
end
 
function std (t)
    local squares, avg = 0, mean(t)
    for k, v in pairs(t) do
        squares = squares + ((avg - v) ^ 2)
    end
    local variance = squares / #t
    return math.sqrt(variance)
end
-----------------------------------------------------

function randomFloat(lower, greater)
    return lower + math.random() * (greater - lower);
end

function shuffle(tbl) -- Credit https://gist.github.com/Uradamus/10323382
  for i = #tbl, 2, -1 do
    local j = math.random(i)
    tbl[i], tbl[j] = tbl[j], tbl[i]
  end
  return tbl
end

-- Credits: https://gist.github.com/jrus/3197011
function uuid() 
    local template ='xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'
    return string.gsub(template, '[xy]', function (c)
        local v = (c == 'x') and math.random(0, 0xf) or math.random(8, 0xb)
        return string.format('%x', v)
    end)
end