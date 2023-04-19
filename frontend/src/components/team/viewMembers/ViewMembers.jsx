/** @format */

import React, { useState, useEffect, useContext } from "react";
import MemberCard from "./MemberCard";
import ReactPaginate from "react-paginate";
import AuthContext from "../../../context/auth/AuthContext";
import { isBrowser } from "react-device-detect";
import { useNavigate, useParams } from "react-router-dom";

import styles from "./ViewMembers.module.css";
import cx from "classnames";

import SearchBox from "./SearchBox";
import SuggestionBox from "./SuggestionBox";
import FilterBox from "./FilterBox";
import MessageBox from "../../messagebox/MessageBox";
import WwcApi from "../../../WwcApi";
import ScrollToTop from "../../scrollToTop/ScrollToTop";
import { ERROR_TEAM_MEMBERS_UNABLE_TO_LOAD } from "../../../Messages";
import { useTeamContext } from "../../../context/team/TeamContext";

let current_year =  new Date().getFullYear();

const sortOptions = {
  NEW: { value: "new", label: "Newest Member", prop: "-date_joined" },
  OLD: { value: "old", label: "Oldest Member", prop: "date_joined" },
  FIRST: { value: "first", label: "First Name (A-Z)", prop: "first_name" },
  LAST: { value: "last", label: "Last Name (A-Z)", prop: "last_name" },
};

const baseFilters = [
  {
    group: "role",
    label: "Role",
    type: "button",
    options: [
      { label: "Director", value: "DIRECTOR", enable: true },
      { label: "Leader", value: "LEADER", enable: true },
      { label: "Volunteer", value: "VOLUNTEER", enable: true },
    ],
  },
  {
    group: "status",
    label: "Status",
    type: "button",
    options: [
      { label: "Active", value: "ACTIVE", enable: true },
      { label: "Inactive", value: "INACTIVE", enable: true }
    ],
  },
  {
    group: "created_at",
    label: "Date Added",
    type: "selection",
    options: [
      { label: "Any time", value: "" },
      { label: "3 months", value: "3months" },
      { label: "6 months", value: "6months" },
      { label: current_year, value: "current_year" },
    ],
  },
];

const ViewMembers = (props) => {
  const navigate = useNavigate();
  const params = useParams();
  const team = parseInt(params.team);
  const { teams } = useTeamContext();
  const defaultUsersPerPage = 12;
  const [users, setUsers] = useState([]);
  const [paginationInfo, setPaginationInfo] = useState({
    pageCount: 0,
    offset: 0,
    userPerPage: 0,
    currentUsers: [],
  });
  const [sortKey, setSort] = useState(sortOptions.NEW);
  const { userInfo } = useContext(AuthContext);
  const isDirector = userInfo.role === "DIRECTOR";
  const userRole = userInfo.role;

  const pageRef = React.createRef();

  const [errorOnLoading, setErrorOnLoading] = useState(false);

  // update pagination info once user data is changed
  useEffect(() => {
    let cardsPerPage = defaultUsersPerPage;
    setPaginationInfo({
      userPerPage: cardsPerPage,
      pageCount: Math.ceil(users.length / cardsPerPage),
      currentUsers: users.slice(0, cardsPerPage),
      offset: 0,
    });
  }, [users]);

  const handlePageClick = (data) => {
    let selected = data.selected;
    let offset = selected * paginationInfo.userPerPage;
    setPaginationInfo({
      offset: offset,
      currentUsers: users.slice(offset, offset + paginationInfo.userPerPage),
      pageCount: paginationInfo.pageCount,
      userPerPage: paginationInfo.userPerPage,
    });
  };

  const handleAddMember = () => {
    navigate("/member/add");
  };

  const onSortSelect = (val) => (e) => {
    setSort(sortOptions[val.toUpperCase()]);
  };

  const getMembersData = async (sort, search, filters) => {
    try {
      let _users = await WwcApi.getMembers(sort, search, filters);
      return _users;
    } catch (error) {
      setErrorOnLoading(true);
      console.log(error);
    }
  };

  const [isOpenSuggestionBox, setIsOpenSuggestionBox] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const [search, setSearch] = useState("");
  const [prevSearch, setPrevSearch] = useState("");
  const onSearch = async (query) => {
    setSearch(query);
    if (query.length === 3) {
      // Get suggestion
      let users = await getMembersData(null, query, null);
      let suggestOptions = users.map((user) => {
        return {
          id: user.id,
          value: user.first_name + " " + user.last_name,
        };
      });
      setSuggestions(suggestOptions);
      setIsOpenSuggestionBox(true);
    } else if (query.length < 3) {
      setSuggestions([]);
    }
  };

  const onBlurSearch = (ev) => {
    setIsOpenSuggestionBox(false);
  };

  const onFocusSearch = () => {
    setIsApplyingFilter(false);
    if (suggestions.length) {
      setIsOpenSuggestionBox(true);
    }
  };

  const onEnterSearch = async (searchStr) => {
    setIsApplyingFilter(false);
    setIsOpenSuggestionBox(false);
    if (!searchStr) {
      setSuggestions([]);
    }
    setPrevSearch(searchStr);
    setSearch(searchStr);
    getUsers(searchStr);
  };

  const onSelectSuggestion = async (selectedUser) => {
    // const match = users.find((user) => {
    //   return user.first_name + " " + user.last_name === selectedUser;
    // });
    // if (match) {
    //   setUsers([match]);
    // }
    setPrevSearch(selectedUser);
    setSearch(selectedUser);
    getUsers(selectedUser);
  };

  const [isApplyingFilter, setIsApplyingFilter] = useState(false);
  const toggleFilterBox = () => {
    setIsApplyingFilter(!isApplyingFilter);
  };

  // create team filter if not chapter member page
  let availableFilters = [...baseFilters];
  let initialFilterStatus = { role: [], status: [], date_joined: [], team: [] };
  if (team === 0) {
    const teamFilter = [{ value: 0, label: "All Teams" }];
    teams.forEach((t) => {
      if (t.id !== 0) {
        teamFilter.push({
          value: t.id,
          label: t.name
        });
      }
    });
    let teamOptions = {
      group: "team",
      label: "Team",
      type: "selection",
      options: teamFilter,
    };
    availableFilters.splice(2, 0, teamOptions);
  } else {
    initialFilterStatus.team = [team];
  }
  if (isDirector) {
    availableFilters[1].options[2] = true;
  }

  const [filterOptions, setFilterOptions] = useState(availableFilters);

  const [filters, setFilters] = useState(initialFilterStatus);
  const onFilterApply = (vals) => {
    const teams = vals.team || [];
    vals.team = teams.filter((val) => {
      return val != 0;
    });
    setPrevSearch(search);
    setFilters(vals);
    toggleFilterBox();
  };

  const onFilterReset = (_filters) => {
    setPrevSearch(search);
    setFilters(_filters);
    toggleFilterBox();
  };

  const onFilterBoxBlur = () => {
    setIsApplyingFilter(false);
  };

  const openFilter = () => {
    setIsOpenSuggestionBox(false);
    if (!isApplyingFilter) {
      setIsApplyingFilter(true);
    }
  };

  useEffect(() => {
    getUsers(search);
  }, [sortKey, filters]);

  const getUsers = async (searchKey) => {
    let sortProp = sortKey.prop;
    let members = await getMembersData(sortProp, searchKey, filters);
    setUsers(members || []);
  };

  return (

  <React.Fragment>
    {errorOnLoading && (
      <div
        className={cx(
          styles["error-container"],
          "d-flex justify-content-center"
        )}
      >
        <MessageBox
          type="Error"
          title="Sorry!"
          message={ERROR_TEAM_MEMBERS_UNABLE_TO_LOAD.replace("{0}", teams[team].name)}
        ></MessageBox>
      </div>
    )}
    
    {!errorOnLoading && (
    <div
      id="viewMemberPage"
      className={cx(styles["view-member-page"])}
      ref={pageRef}
    >
      <div className={styles["view-member-page-list-wrapper"]}>
        <div
          id="functionContainer"
          className={cx(styles["search-container"], "d-flex")}
        >
          <div
            id="filterContainer"
            className={cx(styles["filter-container"], "d-flex")}
          >
            <div className={styles["filter-search-box"]}>
              <SearchBox
                onSearchChange={onSearch}
                onBlur={onBlurSearch}
                onFocus={onFocusSearch}
                onEnter={onEnterSearch}
                value={search}
              ></SearchBox>
            </div>
            <div className={styles["filter-suggestion-box"]}>
              {isOpenSuggestionBox && (
                <SuggestionBox
                  options={suggestions}
                  onSelect={onSelectSuggestion}
                ></SuggestionBox>
              )}
            </div>
            {isBrowser && (
              <button
                className={cx(
                  styles["btn-group-append"],
                  "btn btn-outline-secondary dropdown-toggle"
                )}
                type="button"
                onClick={openFilter}
              >
                Filters
              </button>
            )}
            {isApplyingFilter && (
              <FilterBox
                options={filterOptions}
                state={filters}
                onBlur={onFilterBoxBlur}
                onFilterApply={onFilterApply}
                onFilterReset={onFilterReset}
              ></FilterBox>
            )}
          </div>
          {isBrowser && (
            <div
              id="sortContainer"
              className={styles["sort-container"] + " d-flex dropdown"}
            >
              <div id="sortLabel" className={styles.label}>
                Sort By:
              </div>
              <button
                className={cx(
                  styles["sort-button"],
                  styles["action-button"],
                  "btn dropdown-toggle"
                )}
                type="button"
                id="sortDropdownButton"
                data-bs-toggle="dropdown"
                aria-haspopup="true"
                aria-expanded="false"
                data-offset="{top: 10}"
              >
                {sortKey.label}
              </button>
              <div
                id="sortDropdownMenu"
                className={cx(styles["sort-dropdown"], "dropdown-menu")}
                aria-labelledby="sortDropdownButton"
              >
                <span className={styles["dropdown-menu-arrow"]}></span>
                {Object.values(sortOptions).map((option, idx) => (
                  <button
                    type="button"
                    key={idx}
                    className={cx(
                      styles["sort-dropdown-item"],
                      "dropdown-item",
                      { [styles.active]: option.value === sortKey.value }
                    )}
                    value={option.value}
                    onClick={onSortSelect(option.value)}
                  >
                    {option.label}
                  </button>
                ))}
              </div>
            </div>
          )}
          {isDirector && (
            <div
              id="addMemberButtonContainer"
              className={styles["add-memeber-button-container"]}
              onClick={handleAddMember}
            >
              <button
                type="button"
                id="addMemberButton"
                className={cx(
                  styles["add-member-button"],
                  styles["action-button"],
                  "btn"
                )}
              >
                + Add Member
              </button>
            </div>
          )}
        </div>

        <div className={cx(styles["memberlist-container"], "container px-0")}>
          <div
            className={cx(styles["memberlist-row"], "row", {
              "no-gutters": isBrowser,
            })}
          >

            {!users.length && 
              ((prevSearch.length > 0) ? 
                (<div className={styles["empty-users-msg"]}>
                  No name matching: {prevSearch}
                </div>) : 
                (<div className={styles["empty-users-msg"]}>
                  No members to display
                </div>)) 
            }

            {(isBrowser ? paginationInfo.currentUsers : users).map(
              (userInfo, idx) => {
                return (
                  <React.Fragment key={idx}>
                    <MemberCard
                      userInfo={userInfo}
                      isDirector={isDirector}
                      userRole={userRole}
                      viewClassName={
                        "col-12 col-lg-3 " +
                        ((idx + 1) % 4 > 0 ? styles["memberlist-card-gap"] : "")
                      }
                    />
                    {(idx + 1) % 4 === 0 && (
                      <div className={cx(styles.break, "w-100")}></div>
                    )}
                  </React.Fragment>
                );
              }
            )}
          </div>
        </div>
      </div>
      {isBrowser && users.length > 0 && (
        <div>
          <ReactPaginate
            previousLabel={""}
            nextLabel={""}
            breakLabel={"..."}
            breakClassName={styles["break-me"]}
            previousClassName={styles.previous}
            previousLinkClassName={styles["prev-link"]}
            nextClassName={styles.next}
            nextLinkClassName={styles["next-link"]}
            pageClassName={styles.page}
            pageLinkClassName={styles.link}
            pageCount={paginationInfo.pageCount}
            marginPagesDisplayed={2}
            pageRangeDisplayed={5}
            onPageChange={handlePageClick}
            containerClassName={styles.pagination}
            subContainerClassName={cx(styles.pages, styles.pagination)}
            activeClassName={styles.active}
          />
        </div>
      )}
      <ScrollToTop />
    </div>
    )}
  </React.Fragment>
  ); //end component return
}; // end component definition

export default ViewMembers;
