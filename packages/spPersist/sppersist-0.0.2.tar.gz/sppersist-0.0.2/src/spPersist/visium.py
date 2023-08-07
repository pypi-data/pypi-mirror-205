def visium(gex: str, pos: str):
  '''
  visium takes cell by gene count file name gex and tissue position lists pos, 
  and return an annotated data object with spatial coordinates.
  Note that gex and pos should be formatted as Spance Ranger outputs.
  '''
  ad = sc.read_10x_h5(gex)
  coords = pd.read_csv(pos,index_col=0)
  coords.columns = ["in_tissue", "array_row", "array_col", "pxl_col_in_fullres", "pxl_row_in_fullres"]
  ad.obs = pd.merge(ad.obs, coords, how="left", left_index=True, right_index=True)
  ad.obsm['spatial'] = ad.obs[["pxl_row_in_fullres", "pxl_col_in_fullres"]].values
  ad.obs.drop(columns=["pxl_row_in_fullres", "pxl_col_in_fullres"], inplace=True)
  return ad