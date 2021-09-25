/** @format */

import React, { useState, useEffect, useContext } from "react";
import MemberCard from "./MemberCard";
import ReactPaginate from "react-paginate";
import AuthContext from "../../context/auth/AuthContext";
import { isBrowser } from "react-device-detect";
import { useHistory } from "react-router-dom";

import styles from "./ViewMembers.module.css";
import cx from "classnames";

import SearchBox from "./SearchBox";
import SuggestionBox from "./SuggestionBox";
import FilterBox from "./FilterBox";
import WwcApi from "../../WwcApi";

const sortOptions = {
  NEW: { value: "new", label: "Newest Member", prop: "-date_joined" },
  OLD: { value: "old", label: "Oldest Member", prop: "date_joined" },
  FIRST: { value: "first", label: "First Name (A-Z)", prop: "first_name" },
  LAST: { value: "last", label: "Last Name (A-Z)", prop: "last_name" },
};

const ViewMembers = (props) => {
  const history = useHistory();
  const numOfRows = 3;
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
  const pageRef = React.createRef();

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
    history.push("/member/add");
  };

  const onSortSelect = (val) => (e) => {
    setSort(sortOptions[val.toUpperCase()]);
  };

  const getMembersData = async (sort, search) => {
    try {
      let _users = await WwcApi.getMembers(sort, search);
      return _users;
    } catch (error) {
      console.log(error);
    }
  };

  // TODO: temp function for filtering
  const filterMembers = (users) => {
    const nonemptyFilters = {};
    for (let key in filters) {
      if (filters[key].length) {
        nonemptyFilters[key] = filters[key];
      }
    }
    // no filter applied
    if (!Object.keys(nonemptyFilters).length) {
      return users;
    }
    return users.filter((user) => {
      let match = true;
      Object.keys(nonemptyFilters).forEach((key) => {
        if (match) {
          if (user[key] && !nonemptyFilters[key].includes(user[key].toLowerCase())) {
            match = false;
          }
        }
      });
      return match;
    });
  };

  const [isOpenSuggestionBox, setIsOpenSuggestionBox] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const [search, setSearch] = useState("");
  const onSearch = async (query) => {
    if (query.length === 3) {
      // Get suggestion
      let users = await getMembersData(null, query);
      let suggestOptions = users.map((user) => {
        return {
          id: user.id,
          value: user.first_name + " " + user.last_name
        }
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

  const onEnterSearch = (searchStr) => {
    setIsApplyingFilter(false);
    setIsOpenSuggestionBox(false);
    setSearch(searchStr)
  };

  const onSelectSuggestion = (selectedUser) => {
    const match = users.find((user) => {
      return user.first_name + " " + user.last_name === selectedUser;
    });
    if (match) {
      setUsers([match]);
    }
  };

  const [isApplyingFilter, setIsApplyingFilter] = useState(false);
  const toggleFilterBox = () => {
    setIsApplyingFilter(!isApplyingFilter);
  };

  const [filterOptions, setFilterOptions] = useState([
    {
      group: "role",
      label: "Role",
      type: "button",
      options: [
        { label: "Director", value: "director", enable: true },
        { label: "Leader", value: "leader", enable: true },
        { label: "Volunteer", value: "volunnteer", enable: true },
      ],
    },
    {
      group: "status",
      label: "Status",
      type: "button",
      options: [
        { label: "Active", value: "active", enable: true },
        { label: "Inactive", value: "inactive", enable: true },
        { label: "Pending", value: "pending", enable: isDirector },
      ],
    },
    {
      group: "team",
      label: "Team",
      type: "selection",
      options: [],
    },
    {
      group: "date_joined",
      label: "Date Added",
      type: "selection",
      options: [
        { label: "Any time", value: "anytime" },
        { label: "3 months", value: "3" },
        { label: "6 months", value: "6" },
        { label: "2020", value: "year" },
      ],
    },
  ]);

  const getTeams = async () => {
      let teams = await WwcApi.getTeams();
      teams = teams.map((team) => {
        return {
          value: team.id,
          label: team.name
        }
      });
      let options = [...filterOptions];
      options[2].options = teams;
      setFilterOptions(options);
  };

  useEffect(() => { getTeams() }, [])

  const [filters, setFilters] = useState({ role: [], status: [], date: [] });
  const onFilterApply = (vals) => {
    setFilters(vals);
    toggleFilterBox();
  };

  const onFilterReset = (_filters) => {
    setFilters(_filters);
    //toggleFilterBox();
  };

  const onFilterBoxBlur = () => {
    setIsApplyingFilter(false);
  }

  const openFilter = () => {
    setIsOpenSuggestionBox(false);
    if (!isApplyingFilter) {
      setIsApplyingFilter(true);
    }
  };

  useEffect(() => {
    async function getUsers() {
      let sortProp = sortKey.prop;
      let members = await filterMembers(getMembersData(sortProp, search));
      setUsers(members);
    }
    getUsers()
  }, [sortKey, filters, search]);

  return (
      <div
        id='viewMemberPage'
        className={cx(styles["view-member-page"], "d-flex flex-column")}
        ref={pageRef}
      >
        <div className={styles["view-member-page-list-wrapper"]}>
          <div className={styles["page-label-wrapper"]}>
            {" "}
          </div>
          <div
            id='functionContainer'
            className={cx(styles["search-container"], "d-flex")}
          >
            <div
              id='filterContainer'
              className={cx(styles["filter-container"], "d-flex")}
            >
              <div className={styles["filter-search-box"]}>
                <SearchBox
                  onSearchChange={onSearch}
                  onBlur={onBlurSearch}
                  onFocus={onFocusSearch}
                  onEnter={onEnterSearch}
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
                  type='button'
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
                id='sortContainer'
                className={styles["sort-container"] + " d-flex"}
              >
                <div id='sortLabel' className={styles.label}>
                  Sort By:
                </div>
                <button
                  className={cx(
                    styles["sort-button"],
                    styles["action-button"],
                    "btn dropdown-toggle"
                  )}
                  type='button'
                  id='sortDropdownButton'
                  data-toggle='dropdown'
                  aria-haspopup='true'
                  aria-expanded='false'
                  data-offset='{top: 10}'
                >
                  {sortKey.label}
                </button>
                <div
                  id='sortDropdownMenu'
                  className={cx(styles["sort-dropdown"], "dropdown-menu")}
                  aria-labelledby='sortDropdownButton'
                >
                  <span className={styles["dropdown-menu-arrow"]}></span>
                  {Object.values(sortOptions).map((option, idx) => (
                    <button
                      type='button'
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
                id='addMemberButtonContainer'
                className={styles["add-memeber-button-container"]}
                onClick={handleAddMember}
              >
                <button
                  type='button'
                  id='addMemberButton'
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
              {(isBrowser ? paginationInfo.currentUsers : users).map(
                (userInfo, idx) => {
                  return (
                    <React.Fragment key={idx}>
                      <MemberCard
                        userInfo={userInfo}
                        isDirector={isDirector}
                        viewClassName={
                          "col-12 col-lg-3 " +
                          ((idx + 1) % 4 > 0
                            ? styles["memberlist-card-gap"]
                            : "")
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
        {isBrowser && (
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
      </div>
  );
};

export default ViewMembers;
