import React, { useState, useEffect } from 'react';
import Sidebar from '../../partials/Sidebar';
import Form from '../../components/folders/form';
import Header from '../../partials/Header';
import { getFolder } from '../../services/api';
import { useParams } from 'react-router-dom';
import showError from "../../components/showError";
function FoldersEdit() {
  const { id } = useParams();
  const [name, setName] = useState('');
  const [folder_id, setFolderId] = useState('');



  useEffect(() => {
    getFolder(id)
      .then((data) => {
          setName(data.name);
          setFolderId(data.folder_id);

      })
      .catch((error) => {
        showError(error);
      });
  }, [id]);

  return (
    <div className="flex h-[100vh] overflow-hidden">
      <Sidebar />
      <div className="relative flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
        <Header />
        <main className="grow">
          <div className="px-4 sm:px-6 lg:px-8 py-8 w-full max-w-9xl mx-auto">
            <Form
              name={name}
              folder_id={folder_id}

              id={id}
            />
          </div>
        </main>
      </div>
    </div>
  );
}

export default FoldersEdit;
