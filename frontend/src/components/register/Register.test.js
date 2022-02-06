import React from 'react';
import { render } from '@testing-library/react';
import Register from './Register';
import { createMemoryHistory } from 'history';
import { Router} from "react-router";


test('Tests Register component', () => {
    
        const history = createMemoryHistory({initialEntries: ['/register?email=a@b.com&token=test']});
        let loc = {search: "?email=a@b.com&token=test"};
        const {getByText, getByTestId} = render(
            <Router history={history}>
                <Register location={loc}/>
             </Router>
        )

        const emailInp = getByTestId('register-email');
        const submitBtn = getByTestId('register-submit-button');
        // renders correctly

        expect(getByText(/Register for/i)).toBeInTheDocument();
        expect(getByText(/Chapter Tools/i)).toBeInTheDocument();
        expect(emailInp).toBeInTheDocument();
        expect(emailInp).toHaveAttribute('readOnly');
        expect(emailInp).toHaveAttribute('value','a@b.com');
        expect(submitBtn).toBeInTheDocument();
        expect(submitBtn).toHaveAttribute('disabled');

        // 
        
});