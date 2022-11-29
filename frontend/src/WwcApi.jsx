import axios from "axios";

const BASE_URL =
  process.env.REACT_APP_API_URL ||
  "https://wwcode-chtools-api.herokuapp.com/api";

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
    const { detail, code, error: err } = error.response.data;
    console.log(err);
    console.log("Interceptor error:", detail, ":", code);

    const originalRequest = error.config;

    if (
      error.response.status === 401 &&
      !originalRequest._retry &&
      code === "token_not_valid"
    ) {
      // Access Token expired, get new token using the existing Refresh token
      if (
        sessionStorage.getItem("token") &&
        detail === "Given token not valid for any token type"
      ) {
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
      if (detail === "Token is invalid or expired") {
        console.log(
          "Refresh token expired, cleanup tokens and navigate to Login page"
        );
        sessionStorage.removeItem("token");
        sessionStorage.removeItem("user");
        return (window.location.href = `${BASE_URL}/login`);
      }
    }
    return Promise.reject(error);
  }
);

class WwcApi {
  static async login(data) {
    return await axios.post(`${BASE_URL}/login/`, data, {
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

  static async resetPassword(data) {
    return await axios.patch(`${BASE_URL}/user/reset_password/confirm/`, data, {
      headers: { "Content-Type": "application/json" },
    });
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

  static async getMembers(orderBy, search, filters) {
    let url = `${BASE_URL}/users/?`;

    const searchParams = new URLSearchParams();

    if (orderBy) {
      searchParams.set("ordering", orderBy);
    }
    if (search) {
      searchParams.set("search", search);
    }
    if (filters) {
      for (const prop in filters) {
        for (const filterVal of filters[prop]) {
          searchParams.append(prop, filterVal);
        }
      }
    }

    url += searchParams.toString();
    console.log(url);
    let res = await axios.get(url, {
      headers: getConfig(),
    });
    return res.data;
  }

  static async getMember(userId) {
    let res = await axios.get(`${BASE_URL}/user/${userId}/`, {
      headers: getConfig(),
    });
    return res.data;
  }

  static async createMember(data) {
    return await axios.post(`${BASE_URL}/user/create/`, data, {
      headers: getConfig(),
    });
  }

  static async addInvitee(data) {
    return await axios.post(`${BASE_URL}/invitee/`, data, {
      headers: getConfig(),
    });
  }

  static async activateMember(data) {
    return await axios.post(`${BASE_URL}/user/activate/`, data);
  }

  static async validateInvitation(data) {
    return await axios.get(`${BASE_URL}/validate/`, data);
  }

  static async getTeams() {
    let res = await axios.get(`${BASE_URL}/teams/`, {
      headers: getConfig(),
    });
    return res.data;
  }

  static async editMember(userId, data) {
    return await axios.post(`${BASE_URL}/user/edit/${userId}`, data, {
      headers: getConfig(),
    });
  }

  static async editMemberRoleTeams(userId, data) {
    return await axios.put(`${BASE_URL}/user/edit/${userId}/role_teams/`, data, {
      headers: getConfig(),
    });
  }

  static async getUserProfile() {
    let res = await axios.get(`${BASE_URL}/user/profile/`, {
      headers: getConfig(),
    });
    return res.data;
  }

  static async editUserName(userName) {
    return await axios.patch(`${BASE_URL}/user/name/`, userName, {
      headers: getConfig(),
    });
  }

  static async editUserPassword(data) {
    return await axios.patch(`${BASE_URL}/user/password/`, data, {
      headers: getConfig(),
    });
  }

  static async getTeamResources(slug) {
    return await axios.get(`${BASE_URL}/resources/${slug}/`, {
      headers: getConfig(),
    });
  }

  static async updateTeamResources(slug, links) {
    return await axios.put(`${BASE_URL}/resources/${slug}/`, links, {
      headers: getConfig(),
    });
  }

  static async addNewResources(links) {
    return await axios.post(`${BASE_URL}/resources/`, links, {
      headers: getConfig(),
    });
  }

  static async changeMemberStatus(userId, data) {
    return await axios.post(`${BASE_URL}/user/edit/${userId}/status/`, data, {
      headers: getConfig(),
    });
  }

  static async deleteMemberRole(userId, data) {
    return await axios.delete(`${BASE_URL}/user/edit/${userId}/role/`, data, {
      headers: getConfig(),
    });
  }

  static async getInvitees() {
    let res = await axios.get(`${BASE_URL}/invitee/`, {
      headers: getConfig(),
    });
    return res.data;
  }
}
export default WwcApi;
