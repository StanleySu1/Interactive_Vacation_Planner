import os
import sys
import json
from pyquery import PyQuery as pq

from model import Review, Attraction

def scrape_tripadvisor(path:str) -> Attraction:
  attraction = Attraction()

  d = pq(filename=path)
  for b in d("#lithium-root > main > div:nth-child(1) > div.IDaDx.Iwmxp.mvTrV.cyIij.fluiI.SMjpI > div > div > div"):
    attraction.breadcrumbs.append(d(b).text())
  attraction.name = d("#lithium-root > main > div:nth-child(1) > div.hJiTo.z > div.IDaDx.Iwmxp.mvTrV.cyIij.fluiI.SMjpI > header > div.mmBWG > div.ycuCc > div > h1").text()
  attraction.description = d("#AR_ABOUT > div.afQPz.SyjMH.ttWhi.WRRwX.Gg.A > div > div > div.pqqta._d > div > div.fIrGe._T.bgMZj > div > span").text()
  attraction.category = d("#lithium-root > main > div:nth-child(1) > div.hJiTo.z > div:nth-child(2) > div.EYAyj.z > div > div.C > section:nth-child(2) > div > div > div > div > div:nth-child(1) > div.zCoYj > div > span").text()
  attraction.hours = d("#lithium-root > main > div:nth-child(1) > div.hJiTo.z > div:nth-child(2) > div.EYAyj.z > div > div.C > section:nth-child(2) > div > div > div > div > div:nth-child(2) > div.LdRjT.u > div > div > span").text()
  attraction.duration = d("#AR_ABOUT > div.afQPz.SyjMH.ttWhi.WRRwX.Gg.A > div > div > div.nvXSy.f._Y.Q2 > div:nth-child(2) > div > div").text()
  attraction.address = d("#tab-data-WebPresentation_PoiLocationSectionGroup > div > div > div > div.ZhNYD > div > div > div > div.MJ > button > span").text()
  attraction.neighborhood = d("#tab-data-WebPresentation_PoiLocationSectionGroup > div > div > div > div.ZhNYD > div > div > div > div.MK > div.biGQs._P.fiohW.fOtGX").text()
  for directions in d("#tab-data-WebPresentation_PoiLocationSectionGroup > div > div > div > div.ZhNYD > div > div > div > div.AqkGs > ul > li > div"):
    attraction.getting_there.append(d(directions).text())
  for r in d("#lithium-root > main > div:nth-child(1) > div.hJiTo.z > div:nth-child(2) > div.EYAyj.z > div > div.C > section:nth-child(7) > div > div > div > div.ZHWfd > div > div.wxCXI > div > ul > li > div.bhNjB.Ra.Pk.PY.Px.PK"):
    pr = pq(r)
    review = Review()
    review.title = pr.find("div.biGQs._P.fiohW.qWPrE.ncFvv.fOtGX").text()
    review.review = pr.find("div._T.FKffI.bmUTE > div.fIrGe._T.bgMZj > div > span > div").text()
    review.visited = pr.find("div.xUqsL.mowmC.f.e.Q1 > div:nth-child(1) > span > span").text()
    t = pr.find("#lithium-root > main > div:nth-child(1) > div.hJiTo.z > div:nth-child(2) > div.EYAyj.z > div > div.C > section:nth-child(2) > div > div > div > div > div:nth-child(1) > div:nth-child(1) > a > div > svg > title").text()
    try:
      review.rating = float(t.split(" ")[0])
    except: pass
    attraction.top_reviews.append(review)

  for image in d("#AR_ABOUT > div.FdLSX.MK > div > div > div > div > div.w > div > div.XKYCB.wSSLS > div.ZGLUM.w.H0.mCWMf > button > div > picture > img"):
    attraction.images.append(pq(image).attr("src").split("?")[0])

  for r in d("#tab-review-content > div > div.LbPSX > div > div"):
    pr = pq(r)
    review = Review()
    review.title = pr.find("div > div > div.biGQs._P.fiohW.qWPrE.ncFvv.fOtGX > a > span").text()
    review.review = pr.find("div > div > div._T.FKffI > div.fIrGe._T.bgMZj > div > span > span").text()
    review.visited = pr.find("div > div > div.RpeCd").text()
    t = pr.find("#tab-review-content > div > div.LbPSX > div > div:nth-child(1) > div > div > div > svg > title").text()
    try:
      review.rating = float(t.split(" ")[0])
    except: pass
  return attraction

def process_tripadvisor(src_path:str, out_path:str):
  with open(out_path, "wt") as fh:
    for root, dir, files in os.walk(src_path):
      for file in files:
        attraction = scrape_tripadvisor(os.path.join(root, file))
        fh.write(json.dumps(attraction.model_dump()) + "\n")

if __name__ == "__main__":
  if len(sys.argv) < 3:
    print(f"""Use: {sys.argv[0]} <root folder> <output file>
e.g. {sys.argv[0]} data/sources/tripadvisor data/scraped/tripadvisor.jsonl
""")
    sys.exit(-1)

  process_tripadvisor(sys.argv[1], sys.argv[2])
