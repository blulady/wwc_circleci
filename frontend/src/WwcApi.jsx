import axios from "axios";

const BASE_URL =
  process.env.REACT_APP_API_URL ||
  "https://wwcode-chtools-api-dev.herokuapp.com/api";

const getConfig = () => {
  let { access } = JSON.parse(sessionStorage.getItem("token"));
  return {
    Authorization: `Bearer ${access}`,
    "Content-Type": "application/json",
  };
};

axios.interceptors.response.use(
  (response) => {
    return response;
  },
  function (error) {
    
    const {detail,code, error: err} = error.response.data
    console.log(err);
    console.log('Interceptor error:',detail,':',code)
     
    const originalRequest = error.config;
    
    if (error.response.status === 401 && !originalRequest._retry && code==='token_not_valid'){
      // Access Token expired, get new token using the existing Refresh token
      if (sessionStorage.getItem("token") && detail==='Given token not valid for any token type'){
          originalRequest._retry = true;
          const { refresh } = JSON.parse(sessionStorage.getItem("token"));
          return axios
            .post(`${BASE_URL}/login/refresh`, { refresh: refresh })
            .then((res) => {
              if (res.status === 200) {
                console.log(res);
                let { access, refresh } = res.data;
                let token = { access, refresh };
                sessionStorage.setItem("token", JSON.stringify(token));
                console.log("Access token has been refreshed");
                originalRequest.headers = getConfig();
                return axios(originalRequest);
              } 
            });   
          } 
          // Refresh Token expired. clean up the tokens stored in sessionStorage
          if (detail==='Token is invalid or expired'){
            console.log("Refresh token expired, cleanup tokens and navigate to Login page")
            sessionStorage.removeItem("token");
            sessionStorage.removeItem("user");
            return window.location.href = `${BASE_URL}/login`;
          }   
    }
    return Promise.reject(error);
  }
);

class WwcApi {
  static async login(data) {
    return await axios.post(`${BASE_URL}/login`, data, {
      headers: { "content-type": "application/json" },
    });
  }

  static async sendResetEmail(email) {
    return await axios.post(
      `${BASE_URL}/user/reset_password/request/`,
      { email: email },
      {
        headers: { "content-type": "application/json" },
      }
    );
  }

  static async resetPassword(data){
    return await axios.patch(`${BASE_URL}/user/reset_password/confirm/`, data, {
      headers: { "Content-Type": "application/json" }});
  }

  static async logout() {
    return await axios.post(
      `${BASE_URL}/logout/`,
      {},
      {
        headers: getConfig(),
      }
    );
  }

  static async getMembers(orderBy, search) {
    let url = `${BASE_URL}/users/`;
    if (orderBy) {
      url += "?ordering=" + orderBy;
    }
    if (search) {
      url += (orderBy ? "&" : "?") + "search=" + search
    }
    let res = await axios.get(url, {
      headers: getConfig(),
    });
    return res.data;
  }

  static async getMember(userId) {
    let res = await axios.get(`${BASE_URL}/user/${userId}`, {
      headers: getConfig(),
    });
    return res.data;
  }

  static async createMember(data) {
    return await axios.post(`${BASE_URL}/user/create/`, data, {
      headers: getConfig(),
    });
  }

  static async register(data) {
    return await axios.post(`${BASE_URL}/user/activate/`, data);
  }

  static async getTeams() {
    let res = await axios.get(`${BASE_URL}/teams/`,{
      headers: getConfig(), 
    });
    return res.data;
  }

  static async editMember(data, userId) {
    return await axios.post(`${BASE_URL}/user/edit/${userId}`, data,{
      headers: getConfig(),
    });
  }

  static async getVolunteerResources(slug) {
    let res = await axios.get(`${BASE_URL}/resources/${slug}`, {
      headers: getConfig(),
    });
    return res.data;
  }

  static async changeMemberStatus(userId,data){
    return await axios.post(`${BASE_URL}/user/edit/${userId}/status`, data, {
      headers: getConfig(),
    });
  }

  static async deleteMemberRole(userId,data){
    return await axios.delete(`${BASE_URL}/user/edit/${userId}/role`, data, {
      headers: getConfig(),
    });
  }
}
export default WwcApi;
