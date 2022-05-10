import React, { useEffect, useState } from "react";
import TeamContext from "./TeamContext";
import WwcApi from "../../WwcApi"

// TODO: Temp variable to filter out teams not yet developed
const activeTeams = [5]

const TeamProvider = ({ children }) => {
    const [teams, setTeams] = useState([]);
    const [fetching, setFetching] = useState(true); // TODO: Is there a better way to delay rendering??

    useEffect(() => {
        const fetchTeams = async () => {
            let _teams = [];
            try {
                _teams = await WwcApi.getTeams();
            } catch (e) {
                console.log(e);
            }
            const teamCount = _teams.length - 1
            _teams = _teams.filter((t) => activeTeams.indexOf(t.id) > -1 );
            // TODO: Remove me once backend adds Tech Bloggers team
            _teams.push({ id: teamCount, name: "Tech Bloggers" })
            setTeams([...teams, ..._teams]);
            setFetching(false);
        }
        fetchTeams();
    }, []);

    return (
        <TeamContext.Provider value={ { teams: (fetching ? [] : teams) } }>{children}</TeamContext.Provider>  
    );
}

export default TeamProvider;