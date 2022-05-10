import React from 'react';
import { render } from '@testing-library/react';
import Home from './Home';
import * as TeamContext from '../../context/team/TeamContext';

jest.mock('react-router-dom', () => ({
    useNavigate: () => ({
      navigate: jest.fn()
    })
}));

jest.mock('react', () => {
    const ActualReact = jest.requireActual('react');
    return {
        ...ActualReact,
        useContext: () => ({
            userInfo: {
                email: 'director@example.com',
                first_name: 'John',
                id: 1,
                last_name: 'Smith',
                role: 'DIRECTOR'
            },
            handleRemoveAuth: jest.fn()
        })
    };
});

describe('Home', () => {
    test('it renders without crashing', () => {
        const contextTeams = { teams: [{ id: 1, name: 'Team1' }] };
        jest.spyOn(TeamContext, 'useTeamContext')
        .mockImplementation(() => contextTeams);
        const { container } = render(<Home />);
        expect(container).toMatchSnapshot();
    });
});