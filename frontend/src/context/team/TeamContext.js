import { createContext, useContext } from 'react';

const TeamContext = createContext();

export const useTeamContext = () => useContext(TeamContext);
export default TeamContext;