SELECT 
    fecha,
    local,
    visitante,
    goles_local,
    goles_visitante
FROM "2silver"
WHERE local = 'MEXICO'
   OR visitante = 'MEXICO'
LIMIT 10;
