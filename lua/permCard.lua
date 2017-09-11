--ABSTRACT CLASS

PermCard = {}
PermCard.__index = PermCard
PermCard.spawnClass = nil --Abstract

function PermCard:play(target)
    -- target :: table into which to spawn the dude
    target:add(self.spawnClass)
end