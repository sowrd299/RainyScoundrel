require("agent")
require("permCard")

AgentCard = {}
setmetatable(AgentCard, PermCard)
AgentCard.__index = AgentCard --acts as MT for all instances

AgentCard.spawnClass = Agent --inplementing from premCard

function AgentCard:new(name, cost, thiefVal, spyVal, combatVal)
    local o = PermCard:new(name, cost)
    o.thiefVal = thiefVal -- :: int, how much money he steals
    o.spyVal = spyVal -- :: int, how much info he steals
    o.combatVal = combatVal -- :: int, strength in combat
    setmetatable(o, AgentCard)
    return o
end