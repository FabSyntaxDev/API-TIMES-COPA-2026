from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="Copa do Mundo 2026 API",
    description="API para listagem de grupos e seleções da Copa do Mundo 2026",
    version="1.0.0"
)

# -----------------------------------------------------------------------------
# SCHEMAS (Modelos Pydantic para validação e documentação)
# -----------------------------------------------------------------------------
class Team(BaseModel):
    name: str
    code: str
    continent: str

class Group(BaseModel):
    name: str
    teams: List[Team]

# -----------------------------------------------------------------------------
# DATA (Simulação do Banco de Dados em Memória)
# -----------------------------------------------------------------------------
db_groups = [
    {
        "name": "Grupo A",
        "teams": [
            {"name": "México", "code": "MEX", "continent": "CONCACAF"},
            {"name": "África do Sul", "code": "RSA", "continent": "CAF"},
            {"name": "República da Coreia", "code": "KOR", "continent": "AFC"},
            {"name": "Tchéquia", "code": "CZE", "continent": "UEFA"}
        ]
    },
    {
        "name": "Grupo B",
        "teams": [
            {"name": "Canadá", "code": "CAN", "continent": "CONCACAF"},
            {"name": "Bósnia e Herzegovina", "code": "BIH", "continent": "UEFA"},
            {"name": "Catar", "code": "QAT", "continent": "AFC"},
            {"name": "Suíça", "code": "SUI", "continent": "UEFA"}
        ]
    },
    {
        "name": "Grupo C",
        "teams": [
            {"name": "Brasil", "code": "BRA", "continent": "CONMEBOL"},
            {"name": "Marrocos", "code": "MAR", "continent": "CAF"},
            {"name": "Haiti", "code": "HAI", "continent": "CONCACAF"},
            {"name": "Escócia", "code": "SCO", "continent": "UEFA"}
        ]
    },
    {
        "name": "Grupo D",
        "teams": [
            {"name": "Estados Unidos", "code": "USA", "continent": "CONCACAF"},
            {"name": "Paraguai", "code": "PAR", "continent": "CONMEBOL"},
            {"name": "Austrália", "code": "AUS", "continent": "AFC"},
            {"name": "Turquia", "code": "TUR", "continent": "UEFA"}
        ]
    },
    {
        "name": "Grupo E",
        "teams": [
            {"name": "Alemanha", "code": "GER", "continent": "UEFA"},
            {"name": "Curaçau", "code": "CUW", "continent": "CONCACAF"},
            {"name": "Costa do Marfim", "code": "CIV", "continent": "CAF"},
            {"name": "Equador", "code": "ECU", "continent": "CONMEBOL"}
        ]
    },
    {
        "name": "Grupo F",
        "teams": [
            {"name": "Países Baixos", "code": "NED", "continent": "UEFA"},
            {"name": "Japão", "code": "JPN", "continent": "AFC"},
            {"name": "Suécia", "code": "SWE", "continent": "UEFA"},
            {"name": "Tunísia", "code": "TUN", "continent": "CAF"}
        ]
    },
    {
        "name": "Grupo G",
        "teams": [
            {"name": "Bélgica", "code": "BEL", "continent": "UEFA"},
            {"name": "Egito", "code": "EGY", "continent": "CAF"},
            {"name": "Irã", "code": "IRN", "continent": "AFC"},
            {"name": "Nova Zelândia", "code": "NZL", "continent": "OFC"}
        ]
    },
    {
        "name": "Grupo H",
        "teams": [
            {"name": "Espanha", "code": "ESP", "continent": "UEFA"},
            {"name": "Cabo Verde", "code": "CPV", "continent": "CAF"},
            {"name": "Arábia Saudita", "code": "KSA", "continent": "AFC"},
            {"name": "Uruguai", "code": "URU", "continent": "CONMEBOL"}
        ]
    },
    {
        "name": "Grupo I",
        "teams": [
            {"name": "França", "code": "FRA", "continent": "UEFA"},
            {"name": "Senegal", "code": "SEN", "continent": "CAF"},
            {"name": "Iraque", "code": "IRQ", "continent": "AFC"},
            {"name": "Noruega", "code": "NOR", "continent": "UEFA"}
        ]
    },
    {
        "name": "Grupo J",
        "teams": [
            {"name": "Argentina", "code": "ARG", "continent": "CONMEBOL"},
            {"name": "Argélia", "code": "ALG", "continent": "CAF"},
            {"name": "Áustria", "code": "AUT", "continent": "UEFA"},
            {"name": "Jordânia", "code": "JOR", "continent": "AFC"}
        ]
    },
    {
        "name": "Grupo K",
        "teams": [
            {"name": "Portugal", "code": "POR", "continent": "UEFA"},
            {"name": "RD do Congo", "code": "COD", "continent": "CAF"},
            {"name": "Uzbequistão", "code": "UZB", "continent": "AFC"},
            {"name": "Colômbia", "code": "COL", "continent": "CONMEBOL"}
        ]
    },
    {
        "name": "Grupo L",
        "teams": [
            {"name": "Inglaterra", "code": "ENG", "continent": "UEFA"},
            {"name": "Croácia", "code": "CRO", "continent": "UEFA"},
            {"name": "Gana", "code": "GHA", "continent": "CAF"},
            {"name": "Panamá", "code": "PAN", "continent": "CONCACAF"}
        ]
    }
]

# -----------------------------------------------------------------------------
# ENDPOINTS
# -----------------------------------------------------------------------------

@app.get("/groups", response_model=List[Group], summary="Retorna todos os grupos e seus times")
def get_all_groups():
    return db_groups


@app.get("/groups/{group_letter}", response_model=Group, summary="Busca um grupo específico (Ex: A, B, C...)")
def get_group_by_letter(group_letter: str):
    # Formata a entrada para "Grupo X"
    formatted_name = f"Grupo {group_letter.upper()}"
    
    group = next((g for g in db_groups if g["name"] == formatted_name), None)
    if not group:
        raise HTTPException(status_code=404, detail="Grupo não encontrado. Use letras de A a L.")
    return group


@app.get("/teams", response_model=List[Team], summary="Lista todos os times com opção de filtrar por continente")
def get_all_teams(continent: Optional[str] = None):
    all_teams = []
    for group in db_groups:
        all_teams.extend(group["teams"])
        
    if continent:
        # Filtra os times ignorando maiúsculas/minúsculas
        all_teams = [t for t in all_teams if t["continent"].upper() == continent.upper()]
        if not all_teams:
            raise HTTPException(status_code=404, detail=f"Nenhum time encontrado para o continente: {continent}")
            
    return all_teams
