--IMPLEMENTS INTERFACE: PERMANENT

Agent = {}
local mt = {__index = Agent}

function Agent:new(card)
    local o = {}
    o.card = card -- :: the card which this agent was played from
    o.exh = false 
    setmetatable(o, mt)
end

function AgentCard:exhaust()
    self.exh = true
end

function AgentCard:turn()
    self.unexhaust()
end

function AgentCard:unexhaust()
    self.exh = false
end