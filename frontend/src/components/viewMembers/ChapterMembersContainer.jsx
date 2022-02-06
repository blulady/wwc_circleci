import React, { useState } from 'react'
import ViewMembers from './ViewMembers';
import VolunteerResources from './VolunteerResources';
import ContainerWithNav from "../layout/ContainerWithNav";
import styles from "./ViewMembers.module.css";
import cx from "classnames";

const ChapterMembersContainer = (props) =>{
  const [currentTab, setCurrentTab] = useState('ChapterMembers');
  const tabList = [
    {
      name: 'ChapterMembers',
      label: 'Chapter Members',
      content: (
        <ViewMembers></ViewMembers>
      )
    },
    {
      name: 'VolunteerResources',
      label: 'Volunteer Resources',
      content: (
        <VolunteerResources></VolunteerResources>
      )
    },
  ];
  
  return (
    <ContainerWithNav>
    <div
        id='chapterMemberPage'
        className={cx(styles["view-member-page"], "d-flex flex-column")}
       >
      <div className={styles["chapter-member-page-list-wrapper"]}>
      <div className={styles["page-label-wrapper"]}>      
        <div>
          {
            tabList.map((tab, i) => (
              <button type='button' 
                key={i}
                onClick={() => setCurrentTab(tab.name)} 
                className={(tab.name === currentTab) ? styles["tab-selected-button"] : ''}>
                {tab.label}
              </button>
            ))
          }
        </div>
        {
          tabList.map((tab, i) => {
           if(tab.name === currentTab) {
            return <div key={i}>{tab.content}</div>;
            } else {
            return null;
            }
          })
        }
        </div>
      </div>   
    </div>
    </ContainerWithNav>
  )
};
export default ChapterMembersContainer;