-- Count total matches played
-- Cuenta el total de partidos jugados
SELECT 
    COUNT(*) AS partidos,

    -- Count total wins
    -- Cuenta el total de victorias
    SUM(CASE 
        WHEN local = 'CZECH REPUBLIC' AND goles_local > goles_visitante THEN 1
        WHEN visitante = 'CZECH REPUBLIC' AND goles_visitante > goles_local THEN 1
        ELSE 0
    END) AS victorias,

    -- Calculate win percentage
    -- Calcula el porcentaje de victorias
    ROUND(
        SUM(CASE 
            WHEN local = 'CZECH REPUBLIC' AND goles_local > goles_visitante THEN 1
            WHEN visitante = 'CZECH REPUBLIC' AND goles_visitante > goles_local THEN 1
            ELSE 0
        END) * 100.0 / COUNT(*),
        2
    ) AS porcentaje_victorias,

    -- Calculate total goals scored
    -- Calcula el total de goles anotados
    SUM(CASE 
        WHEN local = 'CZECH REPUBLIC' THEN goles_local
        WHEN visitante = 'CZECH REPUBLIC' THEN goles_visitante
        ELSE 0
    END) AS goles_a_favor,

    -- Calculate total goals conceded
    -- Calcula el total de goles recibidos
    SUM(CASE 
        WHEN local = 'CZECH REPUBLIC' THEN goles_visitante
        WHEN visitante = 'CZECH REPUBLIC' THEN goles_local
        ELSE 0
    END) AS goles_en_contra,

    -- Calculate average goals scored per match
    -- Calcula el promedio de goles anotados por partido
    ROUND(
        SUM(CASE 
            WHEN local = 'CZECH REPUBLIC' THEN goles_local
            WHEN visitante = 'CZECH REPUBLIC' THEN goles_visitante
            ELSE 0
        END) * 1.0 / COUNT(*),
        2
    ) AS goles_favor_por_partido,

    -- Calculate average goals conceded per match
    -- Calcula el promedio de goles recibidos por partido
    ROUND(
        SUM(CASE 
            WHEN local = 'CZECH REPUBLIC' THEN goles_visitante
            WHEN visitante = 'CZECH REPUBLIC' THEN goles_local
            ELSE 0
        END) * 1.0 / COUNT(*),
        2
    ) AS goles_contra_por_partido

-- Source table containing processed match data
-- Tabla fuente con datos procesados de partidos
FROM "2silver"

-- Filter only Czech Republic matches
-- Filtra únicamente partidos de República Checa
WHERE local = 'CZECH REPUBLIC'
   OR visitante = 'CZECH REPUBLIC'
