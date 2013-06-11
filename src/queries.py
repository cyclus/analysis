import tables as tbls

def qAgents(session, fac_t):
    """returns a query of entries in the Agents table given the name of an
    Agent's prototype
    """
    search = tbls.Agents.Prototype == fac_t
    return session.query(tbls.Agents).filter(search)

def nFacs(session, fac_t, time):
    """returns the number of agents of a given type at a given time
    """
    search = tbls.Agents.EnterDate <= time
    entry_rows = qAgents(session, fac_t).filter(search).all()
    entry_ids = set(row.ID for row in entry_rows)

    search = tbls.AgentDeaths.DeathDate > time
    exit_rows = session.query(tbls.AgentDeaths).filter(search).all()
    exit_ids = set(row.AgentID for row in exit_rows)

    return len(entry_ids & exit_ids)
            
def nFacsInRange(session, fac_t, start, end):
    """returns a list of the number of agents at each time step given a starting
    and ending time step
    """
    return [nFacs(session, fac_t, start + i) for i in range(end - start)]

def startMonth(session, simid):
    search = tbls.SimulationTimeInfo.SimId == simid
    result = session.query(tbls.SimulationTimeInfo).filter(search).all()
    assert len(result) == 1
    return result[0].SimulationStart

def endMonth(session, simid):
    search = tbls.SimulationTimeInfo.SimId == simid
    result = session.query(tbls.SimulationTimeInfo).filter(search).all()
    assert len(result) == 1
    return result[0].Duration
