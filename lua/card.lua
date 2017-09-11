--ABSTRACT CLASS

Card = {}
Card.__index = Card

function Card:new(name, cost)
    local o = {}
    o.name = name
    o.cost = cost
    setmetatable(o, Card)
end