-- Count total matches played
-- Cuenta el total de partidos jugados
SELECT 
    COUNT(*) AS partidos,

    -- Count total wins
    -- Cuenta el total de victorias
    SUM(CASE 
        WHEN local = 'SOUTH KOREA' AND goles_local > goles_visitante THEN 1
        WHEN visitante = 'SOUTH KOREA' AND goles_visitante > goles_local THEN 1
        ELSE 0
    END) AS victorias,

    -- Count total draws
    -- Cuenta el total de empates
    SUM(CASE 
        WHEN local = 'SOUTH KOREA' AND goles_local = goles_visitante THEN 1
        WHEN visitante = 'SOUTH KOREA' AND goles_visitante = goles_local THEN 1
        ELSE 0
    END) AS empates,

    -- Count total losses
    -- Cuenta el total de derrotas
    SUM(CASE 
        WHEN local = 'SOUTH KOREA' AND goles_local < goles_visitante THEN 1
        WHEN visitante = 'SOUTH KOREA' AND goles_visitante < goles_local THEN 1
        ELSE 0
    END) AS derrotas,

    -- Calculate win percentage
    -- Calcula el porcentaje de victorias
    ROUND(
        SUM(CASE 
            WHEN local = 'SOUTH KOREA' AND goles_local > goles_visitante THEN 1
            WHEN visitante = 'SOUTH KOREA' AND goles_visitante > goles_local THEN 1
            ELSE 0
        END) * 100.0 / COUNT(*),
        2
    ) AS porcentaje_victorias,

    -- Calculate total goals scored
    -- Calcula el total de goles anotados
    SUM(CASE 
        WHEN local = 'SOUTH KOREA' THEN goles_local
        WHEN visitante = 'SOUTH KOREA' THEN goles_visitante
        ELSE 0
    END) AS goles_a_favor,

    -- Calculate total goals conceded
    -- Calcula el total de goles recibidos
    SUM(CASE 
        WHEN local = 'SOUTH KOREA' THEN goles_visitante
        WHEN visitante = 'SOUTH KOREA' THEN goles_local
        ELSE 0
    END) AS goles_en_contra,

    -- Calculate average goals scored per match
    -- Calcula el promedio de goles anotados por partido
    ROUND(
        SUM(CASE 
            WHEN local = 'SOUTH KOREA' THEN goles_local
            WHEN visitante = 'SOUTH KOREA' THEN goles_visitante
            ELSE 0
        END) * 1.0 / COUNT(*),
        2
    ) AS goles_favor_por_partido,

    -- Calculate average goals conceded per match
    -- Calcula el promedio de goles recibidos por partido
    ROUND(
        SUM(CASE 
            WHEN local = 'SOUTH KOREA' THEN goles_visitante
            WHEN visitante = 'SOUTH KOREA' THEN goles_local
            ELSE 0
        END) * 1.0 / COUNT(*),
        2
    ) AS goles_contra_por_partido

-- Source table containing processed match data
-- Tabla fuente con datos procesados de partidos
FROM "2silver"

-- Filter only South Korea matches
-- Filtra únicamente partidos de Corea del Sur
WHERE local = 'SOUTH KOREA'
   OR visitante = 'SOUTH KOREA'
