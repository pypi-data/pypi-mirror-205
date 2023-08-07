def accession_to_h5(gse: str):
  '''
  accession_to_h5 takes GEO Accession number gse that contains a raw tar file 
  of samples of Spance Ranger outputs, and
  exports a zip file of annotated objects from the Visium samples in the dataset 
  as h5 files.
  '''

  filename = gse+'_RAW.tar'
  url = 'https://ftp.ncbi.nlm.nih.gov/geo/series/GSE'+gse[3:6]+'nnn/'+gse+'/suppl/'+ filename
  wget.download(url) # add progress bar

  tar = tarfile.open(filename)
  sampleids = [s.split('_')[0] for s in list(filter(lambda s: s.endswith('.h5'), tar.getnames()))]
  
  # helper function for extracting a Visium sample
  def extractsample(members, sampleid):
    for tarinfo in members:
      if sampleid in tarinfo.name:
        yield tarinfo

  # helper function for emptying a given directory
  def emptydir(folder):
    for filename in os.listdir(folder):
      file_path = os.path.join(folder, filename)
      try:
          if os.path.isfile(file_path) or os.path.islink(file_path):
              os.unlink(file_path)
          elif os.path.isdir(file_path):
              shutil.rmtree(file_path)
      except Exception as e:
          print('Failed to delete %s. Reason: %s' % (file_path, e))


  visium_path = './visium/'
  h5_path = './h5/'

  if 'visium' not in os.listdir():
    os.mkdir(visium_path)
  if 'h5' not in os.listdir():
    os.mkdir(h5_path)

  emptydir(h5_path)

  for sampleid in sampleids:
    emptydir(visium_path)
    
    # extract files for a given sample id to the visium foler
    tar.extractall(path=visium_path,
                   members=extractsample(tar, sampleid))

    for filename in os.listdir(visium_path):
      if filename.endswith('.h5'):
        gex = visium_path + filename
      elif 'positions' in filename:
        pos = visium_path + filename
    
    adata = visium(gex, pos)

    savefilename = sampleid + '.h5'
    adata.write_h5ad(h5_path+savefilename)
  
  # zip h5 files
  shutil.make_archive('h5.zip', 'zip', h5_path)