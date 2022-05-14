import React, { useEffect, useState } from "react";
import TeamContext from "./TeamContext";
import WwcApi from "../../WwcApi"
import data from "./teamInfo.json"

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
            //_teams = _teams.filter((t) => activeTeams.indexOf(t.id) > -1 );
            // TODO: Remove me once backend adds Tech Bloggers team
            _teams.unshift({ id: 0, name: "Chapter Members" });
            _teams.push({ id: 8, name: "Tech Bloggers" });
            _teams = _teams.map((t, i) => {
                return { ...t, ...data[i]};
            });
            setTeams([..._teams]);
            setFetching(false);
        }
        fetchTeams();
    }, []);

    return (
        <TeamContext.Provider value={ { teams: (fetching ? [] : teams) } }>
            {!fetching && children }
        </TeamContext.Provider>  
    );
}

export default TeamProvider;