import React, { useEffect, useState } from "react";
import TeamContext from "./TeamContext";
import WwcApi from "../../WwcApi"
import data from "./teamInfo.json"


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
            _teams.unshift({ id: 0, name: "Chapter Members" });
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