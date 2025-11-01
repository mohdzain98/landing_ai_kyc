<a id='e05a3cdd-5369-47d4-81de-18b4509332a9'></a>

CAPTURING DEMAND TRANSFERENCE IN RETAIL - A STATISTICAL APPROACH

<a id='eff20ad6-0480-4d4a-8773-4a1ff4a8cc5c'></a>

**Omker Mahalanobish**
Statistical Analyst, Walmart Labs, Bengaluru, India
omker.mahalanobish@walmart.com

<a id='8032bb01-6aea-4763-990c-17d37797f2a5'></a>

**Souraj Mishra**
Statistical Analyst, Walmart Labs, Bengaluru, India
souraj.mishra@walmart.com

<a id='9274994e-d11a-4a35-9490-f23a823f267f'></a>

**Amlan Das**
Statistical Analyst, Walmart Labs, Bengaluru, India
amlan.das@walmart.com

<a id='74091c01-5821-48f1-8dd0-fd9f074e0c34'></a>

Subhasish Misra*
Associate Data Scientist, Walmart Labs, Bengaluru, India
subhasish.misra@walmart.com

<a id='80241b32-c86c-4049-9d87-b9497e2561cd'></a>

## Background:

While an item substitution measure provides for the direction, **demand transference** quantifies the magnitude of demand that may get transferred to an item a) When its substitute is deleted b) When it is introduced in a store and cannibalizes on similar items.

<a id='b485e329-6f42-48a7-80c0-12ba76290f33'></a>

This, hence, is an important input into assortment optimization. If an item is predicted to exhibit a good extent of transference **then we may be more certain of deleting it** (provided, it is less than an average performer in terms of sales). Conversely, we should be careful of deleting a very incremental item (with low demand transference) – since we'll be losing on a bulk of its demand.

<a id='653265bc-f024-42dd-b58b-1130c83edea2'></a>

Note that transference is not explicitly observed, it's latent. Our methodology explains how we capture it.

<a id='51d504b7-2816-47a2-8cc4-4ab80424f6d9'></a>

**Method:**
**Data:** POS, promotions & item attribute data is harnessed for this process.

<a id='214e0572-1c37-45d5-8270-244d910776bc'></a>

## Modeling:

* Regression models (in a longitudinal setup) are used to estimate demand for an item – among other explanatory variables we have one that accounts for cannibalization effect of similar items.
* The cannibalization term uses the attribute data to calculate item similarity. Its value changes depending on presence/absence of similar items and is the instrument through which demand transference seeps into this model.

<a id='cacf26c5-395e-4176-b508-cc80a299cf18'></a>

Electronic copy available at: https://ssrn.com/abstract=3227753

<a id='a801e443-9624-4c3d-a127-b76b27daeb17'></a>

- The modeling process is designed to automatically take care of complications such as multicollinearity and sundry regression violations.
- Since each store is unique in terms of the consumer demand pattern these models have been estimated at a store x substitutable community level.
- This means that for a category with 10 + substitutable community, we are estimating 10 * 4000 + = 40000 + models using parallelization techniques in Hadoop.

<a id='c18ff196-a647-4a81-a04a-fb4db29c82b0'></a>

In conclusion, these models predict the extent of transference (i.e. if an item "i₁" in the pre-delete scenario was selling 100 units, then what amount of its demand would get transferred to its substitutes, say, "i₂", "i₃", "i₄"). All this, at an individual store level as well as the overall US.

<a id='01a7b3c0-4f31-4a0a-87f9-f7d476b8fe66'></a>

**Expected outcome:**

The methodology has been successfully tested for multiple foods and consumable categories, as well as general merchandising categories in the US – efforts are on towards making this one of the processes of estimating demand transference. The entire process, despite involving sophisticated modeling has been **scaled (across all stores)**, **automated and productized** as an easy to use manner for the business user.

<a id='d7a12423-8df1-4b6f-adc0-fd58b5468c7c'></a>

**Keywords:** *Regression, Cannibalization, Retail, Parallelization, Forecasting*

<a id='b768e516-6664-41a0-807f-940da1719ba8'></a>

# 1. INTRODUCTION
Assortment is a key element of a retailer's marketing mix. It differentiates a retailer from its competitors and has a very strong influence on retail sales. Retailers face the problem of selecting the assortment that maximizes category profitability, without sacrificing customer satisfaction.

<a id='b79c4606-36a3-44de-b5fd-419b2bd01c8a'></a>

Although some headway has been made in the context of assortment optimization, practitioners and academics agree that more research is needed to provide feasible solutions to realistic assortment problems. Specifically, the challenge of assortment optimization is compounded by the fact that the demand for an item cannot be assumed to be fixed; it is instead affected by the presence of other items as a result of product substitution.

<a id='d3496310-3344-41ed-959d-93204efadc10'></a>

One of the important challenge is to account for similarity effects: an item is a stronger substitute for similar items than it is for dissimilar items. Demand is also driven by own- and cross-marketing mix instruments such as price, promotion and by heterogeneous preference across stores. Capturing these aspects in a response model is further complicated by the fact that assortments and prices observed in empirical data are unlikely to be exogenous. Finally, retailers have to decide about not only the assortment, but also about the pricing, and these decisions need to be customized at a store level.

<a id='43b8f154-2ff3-4b3e-a82e-6fb6ff88e049'></a>

In the process of optimizing the store assortment, it is important to understand the process of demand transference. Demand transference is defined as the process of transfer of demand among the items in a store, once a change in assortment is realized.

<a id='d2cc0294-5e21-4289-b7ef-fb4c1bb3609d'></a>

In a store, for a given category, there may be two realizations of an assortment change :
1. When one or more items are dropped from the assortment, customers who intended to buy any of the dropped items, might either choose to opt for another 'substitutable' item or walk away from the store, without a purchase.

<a id='3702c367-28b7-4713-8038-caa0cb6e517a'></a>

Electronic copy available at: https://ssrn.com/abstract=3227753

<a id='f2545ea3-e0ff-446d-9ff9-de4f2e191072'></a>

2. When one or more items are introduced into the assortment, customers who purchased any of the new items, might either buy the new item out of impulse or replace purchasing an existing item with the new item.

<a id='c40621fd-3294-4bfd-bd94-e8a1be1dcd11'></a>

A better understanding of this underlying process would help in identifying the optimum assortment for the particular category in the particular store. In this paper, we aim to model the mechanism of demand transference so as to optimize the store assortment, for the category.

<a id='9618a1e8-15db-4596-b576-72a0ff11ff02'></a>

## 2. LITERATURE REVIEW
This section briefly discusses about the studies in place related to assortment selection / optimization.

<a id='63ed98fa-1b3e-4b88-903f-e6e45b64b079'></a>

The common points among the available literatures is that they all look to optimize the assortment, based on maximizing cost function (usually sales or profit). We here would only restrict ourselves towards those studies which deal with the item attributes along with the scanner data.

<a id='76d385f4-0b0a-47c2-8460-73bc5b5babdd'></a>

Among the available articles, Fisher and Vaidyanathan (Fisher et al., 2009) look into selecting the optimum number of items from the available lot, to maximize sales. They have defined an approach, in which they view a item as a set of attribute values, use sales history of the items currently carried by the retailer to estimate the demand for each of the attribute values and from this, the demand for any potential item currently not carried by the retailer. They also introduce a model of substitution behavior, estimate the parameters and consider the impact of substitution in choosing assortment.

<a id='7f1fc787-b26d-426c-85c9-3b46c7b00063'></a>

Kök and Fisher (2007), also tread similar lines wherein they study an assortment planning model in which consumers might accept substitutes when their favorite product is unavailable. They develop an algorithmic process to help retailers compute the best assortment for each store, by estimating the parameters of substitution behavior and demand for products at a store, including products that have not been carried previously in that store. Finally, they propose an iterative optimization heuristic to solve the assortment planning problem.

<a id='87445c05-7c72-4c28-af1b-6a78d1860aec'></a>

Other articles like Rooderkerk et al., (2013) look into price optimization along with promotion and shelf space optimization. Herein, they adopt a scalable assortment optimization method that allow for theory based substitution patterns and cross marketing mix effects. For the optimization part, they propose a large neighborhood search heuristic methodology.

<a id='8cc1d514-a5cc-4b3f-a2c4-ff24b30c9bc4'></a>

Our study though on similar lines, addresses an entirely different aspect of assortment study. This is more of scenario based, to understand how the store assortment performs when a change in the store assortment is realized. Basically, we help the retailer to decide which items to drop from the assortment, by helping him understand where the demand of the deleted item would flow to and in what magnitude. The retailer also gets a glimpse of additional incremental demand as well as the magnitude and direction of cannibalization that might be realized when additional items are added to the assortment. In the process of obtaining these insights, he also gets an understanding as to how the items in the new assortment will perform in the future.

<a id='731c0984-3e17-4f2d-ad3d-a4bee772e625'></a>

### 3. METHODOLOGY
Demand is a latent feature, which can be experienced but not explicitly observed. Thus, modeling of demand and validation of the same becomes difficult. The nearest proxy to demand is sales. So, here we try to model the sales of each of the products offered in an assortment.

<a id='4d400cae-b3dd-41aa-8805-e6cf5f3b9669'></a>

Our methodology consists of a sales model, described in section 3.1 and a predictive algorithm based on the sales model, as described in section 3.2.

<a id='a1f1e8a5-f850-414e-8479-71373479fa67'></a>

Electronic copy available at: https://ssrn.com/abstract=3227753

<a id='975f8110-4e39-4897-bdc2-55cb4aec2b0e'></a>

### 3.1. Sales model

Before formulating the model, we look at a significant challenge encountered while developing the sales model: modeling store level UPC sales on attributes. UPC (Universal Product Code) is used to identify trade items in stores across different retailers and markets. UPC is aggregation of items which can vary across different regions.

<a id='80550647-2743-417f-8a76-cbd331fc1fc0'></a>

### 3.1.1. Modeling framework
To model UPC sales at a store level, we chose store-level scanner data, as it provides a holistic view of the available assortment in the store. An example of the input data is provided in Table 1 under section 4.1. Our approach of modeling UPC sales on UPC attributes is motivated by the assertion that customers do not form preference of each individual UPC in a product category but that these preferences are derived from the preferences for the underlying attributes (e.g., size, brand, flavor, etc.). Theoretical justification of the same is available in economics (Lancaster, 1971) and psychology (Fishbein, 1967).

<a id='7b2e5fc7-0b4e-43ea-bf06-231e456a2907'></a>

Our model thus takes into account the UPC attributes, in order to model UPC sales. Apart from the UPCs own attributes, attributes of other available UPCs would also affect the sales. We thus incorporate variables to account for a UPCs attribute similarity as well as cross attribute similarity with the other UPCs in the assortment.

<a id='2711820e-194b-467c-9cf2-fb52cf1bfb61'></a>

### 3.1.2. Modeling formulation
We would now develop the attribute based model and highlight the role similarity variables play. While modeling UPC sales at a store level, we allow for flexible substitution patterns, and non-linear effects by starting with a log-log model (Rooderkerk et al., 2013), similar to the SCAN*PRO model (Wittink et al., 1988):

log($S_{kti}$) = $\underbrace{\alpha_{ki}}_{A}$ + $\underbrace{\beta.log(P_{kti})}_{B}$ + $\underbrace{\sum_{m \in A} \gamma_{kmti}}_{C}$ (1)

<a id='1af7430c-4ede-4ae6-bfc0-077d85773139'></a>

where,

$S_{kti}$ = unit sales of UPC $k \in \{1, 2, ..., K\}$ in week $t \in \{1, 2, ..., T\}$ in store $i \in \{1, 2, ..., n\}$;

$\alpha_{ki}$ = UPC-store intercept for UPC $k \in \{1, 2, ..., K\}$ in store $i \in \{1, 2, ..., n\}$;

$P_{kti}$ = price of UPC $k \in \{1, 2, ..., K\}$ in week $t \in \{1, 2, ..., T\}$ in store $i \in \{1, 2, ..., n\}$;

$\gamma_{kmti}$ = similarity score of UPC $k \in \{1, 2, ..., K\}$, for attribute $m \in \mathcal{A}$, in week $t \in \{1, 2, ..., T\}$ in store $i \in \{1, 2, ..., n\}$;

$\mathcal{A}$ = set of all attributes, evaluated for all UPCs in a product category;

<a id='24f33326-16d6-45ff-81ef-4dc3063d33bb'></a>

Further, $\alpha_{ki}$ may be replaced by strictly store level intercepts along with attribute dummies such that

$\alpha_{ki} = \underbrace{\alpha_i}_{A} + \underbrace{\sum_{m \in A} \sum_{l=1}^{m_l} A_{kml}}_{B}$ (2)

<a id='4c7e9dc0-bf23-43ac-94a0-300764fd1246'></a>

where,

&nbsp;&nbsp;&nbsp;&nbsp;A_kml = 1 if UPC k possesses level l of attribute m ∈ A, and 0 otherwise, if m is nominal

&nbsp;&nbsp;&nbsp;&nbsp;A_kml = the realization of attribute m ∈ A, if m is metric

<a id='6f0baf0c-fb34-4678-9006-c5eca3a1096e'></a>

Electronic copy available at: https://ssrn.com/abstract=3227753

<a id='08d3debb-8619-4557-905c-4251fdb14b67'></a>

### 3.1.3. Attribute similarity score
The similarity score of UPC _k_, for a nominal or metric attribute _m_, in week _t_, in store _i_ is defined such that it varies between 0 (minimum similarity) and 1 (maximum similarity), and also reflects the similarity of UPC _k_ relative to the distribution of attribute _m_ in the entire available assortment.

<a id='6dd8b606-2ac7-4573-a608-69381e98f943'></a>

Let $SIM_{kk'mti}$ denote the magnitude of similarity between UPC $k$ and UPC $k'$ with respect to attribute $m$ in store $i$ in week $t$.

<a id='1baedf2c-f20d-4819-81d6-c2425f064abe'></a>

Further to the above discussed features of similarity, if UPC k and UPC k' share the same level of nominal attribute m, then the perceived similarity of UPC k and UPC k' should be stronger when their shared attribute level occurs less frequently (Goodall, 1966). We obtain all the above, by defining :

<a id='3c3c6171-7b09-4b9b-a6b0-edae4f0a6b49'></a>

$$SIM_{kk'mti} = I\{A_{k'm} = A_{km}\}. \left(1 - \frac{1}{N_{ti}} \sum_{k''=1, x_{k''ti}=1}^{K} I\{A_{k''m} = A_{km}\} \right) \quad (3a)$$

<a id='c659202a-3d6b-4c35-9a30-abea5672f1b4'></a>

if attribute _m_ is nominal, where,

I{·} = an indicator function which takes the value 1 if its argument holds, 0 otherwise;

_A_<sub>_km_</sub> = the level attained by UPC _k_ on attribute _m_ such that _A_<sub>_km_</sub> = _l_ ⇔ _A_<sub>_kml_</sub> = 1;

_N_<sub>_ti_</sub> = the number of UPCs present in week _t_ in store _i_;

_x_<sub>_kti_</sub> = 1, if UPC _k_ was available in store _i_, for at least 1 day in week _t_; else 0.

<a id='dd4dd124-e4da-4ebf-9681-9aca1c2d4564'></a>

Table 3 in section 4.2 illustrates how this would work for a Brand attribute.

<a id='030b3446-defc-4074-a7ba-e4a7559555ec'></a>

On the other hand, the similarity of UPC k and UPC k', with respect to a metric attribute m, is perceived to be more if there exists fewer UPCs with attribute values between the attribute values of UPC k and UPC k'. This is obtained by defining:

<a id='c1e26305-2f4d-4c44-aad9-efcf102605b1'></a>

$$SIM_{kk'mti} = 1 - \frac{1}{N_{ti}} \cdot \sum_{\substack{k''=1 \\ x_{k''ti}=1}}^{K} I\{\min(A_{km}, A_{k'm}) \leq A_{k''m} \leq \max(A_{km}, A_{k'm})\} \quad (3b)$$

<a id='158bb863-ff42-481d-a328-f2bc98382b8d'></a>

if attribute _m_ is metric.
This definition is numerically illustrated for Weight attribute in Table 5 in section 4.2.

<a id='36cc01fa-958b-410a-b053-f89c3c4f0c78'></a>

Once we have described the measure of similarity for UPC k and UPC k', we may now formulate the similarity score of UPC k for attribute m in week t in store i as:

$\gamma_{kmti} = mean^*_{k'\neq k} (SIM_{kk'mti})$

(4)

<a id='236e5b12-cdc1-4caf-8c65-fbaadc5d9acb'></a>

where,
$mean^*(.) = \text{Arithmetic Mean of the non-zero elements of the argument, if attribute } m \text{ is}$
nominal, usual Arithmetic Mean otherwise.

<a id='da7ad285-6388-4021-bbb7-a2e27fa2eeda'></a>

### 3.1.4. Model implementation
The model described in this paper, is best implemented when modeled category wise. Now, each category has properties of its own and consists of widely different varieties of UPCs. The two major category properties that is observed is as follows:

<a id='ef7f4990-8aa0-4863-b7a4-c1909916e142'></a>

1. Demand might get transferred to any and every UPC of the category and

<a id='66d9ccae-fc7b-4bbb-b303-fd185c46c854'></a>

Electronic copy available at: https://ssrn.com/abstract=3227753
Electronic copy available at: https://ssrn.com/abstract=3227753

<a id='71d856d4-96ff-4e63-95b2-51c0d8de2468'></a>

2. Transfer of demand is restricted only within mutually exclusive and exhaustive set of substitutable groups, which are very different from each other (further discussed in section 4.3).

<a id='1ea769f9-e4bf-4853-86e3-e868f383b440'></a>

For case 2, one may carry on the same analysis over each substitutable group, as if assuming it to be a small sized category of sorts.

<a id='4f0b3051-a5f9-48d9-a28e-d6d6733afb7d'></a>

Since we have formulated a linear regression as mentioned in (1), all regression sanity checks have been taken care of and the final model thus only consists of the uncorrelated and significant regressors among the ones mentioned in (1).

<a id='6d2b08ef-29a9-4f3c-b75e-d058d1a88f59'></a>

## 3.2. Predictive algorithm
We would now look into how to predict the magnitude of demand transference and the walkoff rate.
Define

<a id='444f54ec-b0ca-4375-a69b-a172e70d4e40'></a>

A_i : the training assortment of store i;
A'_i : the assortment of store i after the assortment change;

<a id='c3b05585-4211-4533-811e-cf33db33c12b'></a>

Now, for every UPC in A_t, we can easily obtain the predicted weekly unit sales from the model as explained in (1).

<a id='1b8351d9-6fd0-4a46-89af-136e52e462dd'></a>

Also, the values of parts A and B in (1) are independent of the store assortment (assuming there is no change in price in any of the items in Aᵢ) and thus doesn't change. It suffices to compute these values only for those UPCs that have been introduced in A'ᵢ but were not a part of Aᵢ. Part C in (1) directly depends upon the current assortment in store and hence the similarity score is recalculated for each UPC in the new assortment. Once we have all the required information, the predicted weekly unit sales of every UPC in Aᵢ can be easily obtained.

<a id='0cd0c23e-450f-4713-9f67-271b1d4d0d63'></a>

Define,

$\hat{S}_{ki}$ = predicted weekly unit sales of UPC $k \in A_i$;

$\hat{S}'_{ki}$ = predicted weekly unit sales of UPC $k \in A'_i$;

<a id='3882560e-0a9a-4aa1-8722-3d0f5f5d36dc'></a>

Therefore,

<a id='3b62600a-b7d3-4969-a39f-a211819e5aca'></a>

$\Delta S_{ki} = \hat{S}'_{ki} - \hat{S}_{ki}$, is the change in the weekly unit sales of UPC $k \in A_i \cap A'_i$.
But, $\Delta S_{ki} = \hat{S}'_{ki}$, if UPC $k \in A'_i \setminus A_i$

<a id='0a3047cd-ff92-4030-a1c6-a4d75104e7ad'></a>

### 3.2.1. Case of item deletion
Define $U_{del}$ = set of UPCs that have been deleted from $A_i$, and are not present in $A'_i$. Then,

<a id='eea88c95-7cf3-47ac-83e6-259b3f968d2d'></a>

$\Delta_{kA'i}^{del} = \frac{\Delta S_{ki}}{\sum_{t \in u_{del}} \hat{S}_{ti}} . 100 \%$ (5a)

<a id='5b9d1001-0c44-4c97-b52c-e61d9a180610'></a>

where,

<a id='8b811637-815e-4882-8f4f-d8f8d7b2c8bb'></a>

$\Delta_{kA'_i}^{del}$ = demand of UPCs in $U_{del}$ transferred to UPC $k$, $\forall k \in A'_i$.

<a id='01e2faf3-a6fe-471b-929a-36d0d39c176f'></a>

Herein, the walk-off rate is calculated as:
$ω_{A'_i}^{del} = 100 - \sum_{k \in A'_i} Δ_{kA'_i}^{del}$ (5b)

<a id='1b54e597-c0fe-476e-a741-a912f6dc24cd'></a>

### 3.2.2. Case of item addition
Define, U_add = set of UPCs that have been added to A'_i, but were not a part of A_i. Then,

<a id='9135034c-1025-4550-b9cf-279622fbdce8'></a>

Electronic copy available at: https://ssrn.com/abstract=3227753

<a id='b0328bed-a677-4350-b02e-2cbdd512bb53'></a>

$$\Delta_{k A'_i}^{add} = \frac{|\Delta S_{ki}|}{\sum_{t \in u_{add}} \hat{S}_{ti}'} \cdot 100 \%$$ (6a)

<a id='b2afa075-8d36-4540-bfe5-9eb99d9aab0c'></a>

where,

<a id='ef6f5850-994a-4f8b-9f95-0dfeb9d74613'></a>

$\Delta_{kA'_i}^{add} = \text{demand of UPCs in } U_{add} \text{ cannibalized from UPC } k, \forall k \in A'_i.$

<a id='94985950-02eb-4257-9554-4c0428155bf3'></a>

Herein, the incrementality is calculated as:

$$\omega_{A'_i}^{add} = 100 - \sum_{k \in A'_i} \Delta_{kA'_i}^{add} \quad (6b)$$

<a id='3f4a84f6-a735-4646-bfe2-81f47ccfc4aa'></a>

### 3.2.3. Case of both item deletion and item addition
In this case, it becomes difficult to identify separately, what amount of the change in the demand for UPC _k_, is due to the transfer of demand from the deleted UPCs and how much amount is due to cannibalization of the added UPCs. Further, there could even be some amount of demand transference towards the newly added UPCs as well.

<a id='5dba4aab-3abe-4f79-a8a1-0576d88f4a44'></a>

Hence, one may separately consider the deletions and additions to obtain the demand transference measures.

<a id='aa44c6c4-2a70-4dc4-ad21-b78f19387103'></a>

Therefore, we have

<a id='d3195ab0-ba43-4bdb-b021-ee01d8e0b97e'></a>

$$\Delta_{K A'_i}^{add} = \frac{|\Delta S_{ki}| \cdot |\mathcal{U}_{add}|}{|\mathcal{U}_{del}| \cdot \sum_{t \in \mathcal{U}_{add}} \hat{S}_{ti}} \cdot 100 \%, \forall k \in A'_i \quad (7a)$$

<a id='09143b66-2e34-43c1-8f50-44316f4776c7'></a>

$$\Delta_{kA'i}^{del} = \frac{\Delta S_{ki} \cdot \frac{|U_{del}|}{|U_{add}|}}{\sum_{t \in U_{del}} \hat{S}_{ti}} \cdot 100\%, \quad \forall k \in A'_i \quad (7b)$$

<a id='07566c17-275c-45d3-807c-9fad1a65402d'></a>

where,

$\Delta_{kA'_i}^{add}$ = demand of UPCs in $U_{add}$ cannibalized from UPC $k$, $\forall k \in A'_i$.

$\Delta_{kA'_i}^{del}$ = demand of UPCs in $U_{del}$ transferred to UPC $k$, $\forall k \in A'_i$.

<a id='3be1fb21-55a2-45d2-b5a9-93d8073d0ed0'></a>

In (7b),

$ΔS_{ki} = ΔS_{ki} · (1 - \sum_{t∈\mathcal{U}_{add}} \frac{Δ_{tA^i}^{add}}{100} · I\{k ∈ \mathcal{U}_{add}\})$ (7c)

<a id='c86cb512-3064-4199-b64f-3d86808b330f'></a>

Therefore, walkoff rate is:

$\omega_{A'_i}^{del} = 100 - \sum_{k \in A'_i} \Delta_{kA'_i}^{del}$

(7d)

<a id='fd2eb0e9-b705-47f7-a0f0-a94d6f30120c'></a>

and incrementality is defined as:

<a id='ed6b1fdb-e88e-485f-953b-3ce676e949c3'></a>

$$\omega_{A'_i}^{add} = 100 - \sum_{k \in A'_i} \Delta_{kA'_i}^{add} - \sum_{k \in \mathcal{U}_{add}} \Delta_{kA'_i}^{del} \quad (7e)$$

<a id='c3b3a45b-5dc9-46a7-b896-ff89f17d6363'></a>

4. DISCUSSION

<a id='44a85855-e5e0-4e3f-9e3f-e778981d1693'></a>

Electronic copy available at: https://ssrn.com/abstract=3227753
Electronic copy available at: https://ssrn.com/abstract=3227753

<a id='46fe3e8e-ffa6-4540-9a83-38a9dcf0a74c'></a>

Here, we will have a brief walkthrough of a sample input data for the algorithm along with the similarity calculation for the same.

<a id='5c92272c-643f-478d-932e-6134d66346d1'></a>

## 4.1. Scanner data and attribute data
Table 1 refers to a snapshot of the scanner data that we require to carry on with the analysis.
The snapshot here has been restricted to 4 UPCs, in 3 weeks and 1 store.

<a id='ba3fed6c-0ab1-46b6-b217-2aadea1fab6d'></a>

Table 1 Snapshot of the scanner data
<table id="7-1">
<tr><td id="7-2">Store No.</td><td id="7-3">UPC</td><td id="7-4">Week No.</td><td id="7-5">Units sold</td><td id="7-6">Dollar Sales</td><td id="7-7">Price</td><td id="7-8">Days available</td></tr>
<tr><td id="7-9">1</td><td id="7-a">UPC 1</td><td id="7-b">1</td><td id="7-c">2</td><td id="7-d">2.40</td><td id="7-e">1.20</td><td id="7-f">7</td></tr>
<tr><td id="7-g">1</td><td id="7-h">UPC 1</td><td id="7-i">2</td><td id="7-j">3</td><td id="7-k">3.55</td><td id="7-l">1.18</td><td id="7-m">7</td></tr>
<tr><td id="7-n">1</td><td id="7-o">UPC 1</td><td id="7-p">3</td><td id="7-q">2</td><td id="7-r">2.40</td><td id="7-s">1.20</td><td id="7-t">7</td></tr>
<tr><td id="7-u">1</td><td id="7-v">UPC 2</td><td id="7-w">1</td><td id="7-x">6</td><td id="7-y">4.50</td><td id="7-z">0.75</td><td id="7-A">6</td></tr>
<tr><td id="7-B">1</td><td id="7-C">UPC 2</td><td id="7-D">2</td><td id="7-E">7</td><td id="7-F">5.25</td><td id="7-G">0.75</td><td id="7-H">7</td></tr>
<tr><td id="7-I">1</td><td id="7-J">UPC 2</td><td id="7-K">3</td><td id="7-L">2</td><td id="7-M">1.60</td><td id="7-N">0.80</td><td id="7-O">7</td></tr>
<tr><td id="7-P">1</td><td id="7-Q">UPC 3</td><td id="7-R">1</td><td id="7-S">0</td><td id="7-T">0.00</td><td id="7-U"></td><td id="7-V">0</td></tr>
<tr><td id="7-W">1</td><td id="7-X">UPC 3</td><td id="7-Y">2</td><td id="7-Z">3</td><td id="7-10">4.50</td><td id="7-11">1.50</td><td id="7-12">3</td></tr>
<tr><td id="7-13">1</td><td id="7-14">UPC 3</td><td id="7-15">3</td><td id="7-16">1</td><td id="7-17">1.50</td><td id="7-18">1.50</td><td id="7-19">4</td></tr>
<tr><td id="7-1a">1</td><td id="7-1b">UPC 4</td><td id="7-1c">1</td><td id="7-1d">10</td><td id="7-1e">6.00</td><td id="7-1f">0.60</td><td id="7-1g">7</td></tr>
<tr><td id="7-1h">1</td><td id="7-1i">UPC 4</td><td id="7-1j">2</td><td id="7-1k">8</td><td id="7-1l">4.80</td><td id="7-1m">0.60</td><td id="7-1n">7</td></tr>
<tr><td id="7-1o">1</td><td id="7-1p">UPC 4</td><td id="7-1q">3</td><td id="7-1r">2</td><td id="7-1s">1.24</td><td id="7-1t">0.62</td><td id="7-1u">2</td></tr>
</table>

<a id='714c9fef-dbbc-47fe-84d9-09b90594c6d1'></a>

Table 2 Attribute information for UPCs in the snapshot
<table id="7-1v">
<tr><td id="7-1w">UPC</td><td id="7-1x">Brand</td><td id="7-1y">Weight (in gm)</td></tr>
<tr><td id="7-1z">UPC 1</td><td id="7-1A">Brand 1</td><td id="7-1B">200</td></tr>
<tr><td id="7-1C">UPC 2</td><td id="7-1D">Brand 1</td><td id="7-1E">180</td></tr>
<tr><td id="7-1F">UPC 3</td><td id="7-1G">Brand 1</td><td id="7-1H">200</td></tr>
<tr><td id="7-1I">UPC 4</td><td id="7-1J">Brand 2</td><td id="7-1K">150</td></tr>
</table>

<a id='6115474f-11a6-49b0-bc50-d3ab66840176'></a>

**4.2. Computing the attribute similarity score**
As depicted in Table 2, there are two attributes to take care of viz. Brand (a nominal attribute) and Weight (a metric attribute).

<a id='f7bdee10-ca09-439f-ba5f-ab5d3aa06fd8'></a>

For attribute Brand, Brand 1 is present in 75% of the overall assortment, whereas Brand 2 is present in 25% of the overall assortment.

<a id='9ef68b04-c6a5-4233-9b0a-da8314bad8c3'></a>

Electronic copy available at: https://ssrn.com/abstract=3227753

<a id='3639b4eb-95d1-403a-80c3-f54bb26adead'></a>

Hence, according to this example, the similarity scores for UPC 1 with respect to the nominal attribute Brand is demonstrated in Table 3 below:

<a id='9de73b5c-14ac-4b1a-925a-bc99728cf532'></a>

Table 3 Week wise brand similarity score for UPC 1
<table id="8-1">
<tr><td id="8-2">Week No.</td><td id="8-3">Brand 1 presence</td><td id="8-4">Brand similarity score (γkmti)</td></tr>
<tr><td id="8-5">1</td><td id="8-6">66.67%</td><td id="8-7">0.33</td></tr>
<tr><td id="8-8">2</td><td id="8-9">75.00%</td><td id="8-a">0.25</td></tr>
<tr><td id="8-b">3</td><td id="8-c">75.00%</td><td id="8-d">0.25</td></tr>
</table>

<a id='5dcfc1bb-d0f9-40f7-a743-72bb6f613938'></a>

Similarly, for the metric attribute Weight, similarity score of UPC 1 is seen to be as described in Table 5 below:

<a id='6b0e691c-a978-4d4b-88af-295f9cf8daf0'></a>

**Table 4** Weekly weight proximity percent for each UPC
<table id="8-e">
<tr><td id="8-f">UPC</td><td id="8-g">Week No.</td><td id="8-h">Weight proximity percent</td><td id="8-i">Weight similarity score</td></tr>
<tr><td id="8-j">UPC 2</td><td id="8-k">1</td><td id="8-l">66.67 %</td><td id="8-m">0.33</td></tr>
<tr><td id="8-n">UPC 2</td><td id="8-o">2</td><td id="8-p">75.00 %</td><td id="8-q">0.25</td></tr>
<tr><td id="8-r">UPC 2</td><td id="8-s">3</td><td id="8-t">75.00 %</td><td id="8-u">0.25</td></tr>
<tr><td id="8-v">UPC 3</td><td id="8-w">1</td><td id="8-x">–</td><td id="8-y">–</td></tr>
<tr><td id="8-z">UPC 3</td><td id="8-A">2</td><td id="8-B">75.00 %</td><td id="8-C">0.25</td></tr>
<tr><td id="8-D">UPC 3</td><td id="8-E">3</td><td id="8-F">75.00 %</td><td id="8-G">0.25</td></tr>
<tr><td id="8-H">UPC 4</td><td id="8-I">1</td><td id="8-J">100.00 %</td><td id="8-K">0.00</td></tr>
<tr><td id="8-L">UPC 4</td><td id="8-M">2</td><td id="8-N">100.00 %</td><td id="8-O">0.00</td></tr>
<tr><td id="8-P">UPC 4</td><td id="8-Q">3</td><td id="8-R">100.00 %</td><td id="8-S">0.00</td></tr>
</table>

<a id='287d946c-76ea-4f10-adb5-7b6deb9b9f03'></a>

Therefore,
<table id="8-T">
<tr><td id="8-U" colspan="2">Table 5 Weekly weight similarity score for UPC 1</td></tr>
<tr><td id="8-V">Week No.</td><td id="8-W">Weight Similarity score</td></tr>
<tr><td id="8-X">1</td><td id="8-Y">0.165</td></tr>
<tr><td id="8-Z">2</td><td id="8-10">0.250</td></tr>
<tr><td id="8-11">3</td><td id="8-12">0.250</td></tr>
</table>

<a id='221269c5-1e10-4209-a190-f5acfe8bec74'></a>

### 4.3. Substitutable groups
A category can be divided into mutually exclusive and exhaustive groups of items, called substitutable groups. A substitutable group consists of items that are more likely to be substitutes of each other, than that of items in the other substitutable groups.

<a id='42b0943d-aebd-4dde-b795-ace0294cf32b'></a>

Electronic copy available at: https://ssrn.com/abstract=3227753

<a id='c6e76cc8-9c4a-43d7-af03-f15a4aa05258'></a>

We accomplish this segmentation into substitutable group by using a proprietary graph partition based algorithm.

<a id='3633e81e-c661-413d-8152-6912fbfeec78'></a>

When, implemented for a substitutable group, the demand transfer algorithm restricts the transfer of demand within the same group; since by definition, there is very less probability of items in other groups to be proper substitutes.

<a id='04a28676-3416-4c0c-88e5-1d2dfc2b2589'></a>

## 4.4. Parallelization techniques
The entire algorithm was executed in R, for a category with 7 substitutable groups, available in 4500 stores.

<a id='fb93129a-65ea-4fe9-b0cf-8fe950eedfdf'></a>

While *Hadoop streaming* was used to execute the algorithm over stores; for a store, the *mclapply* function (which uses forking technique) from *parallel* package was used to parallelize over substitutable groups.

<a id='92161a36-4f64-40b9-a741-d2cd054f4d39'></a>

For a fixed store, the runtime in R (using forking via _mclapply_) is comparable to the runtime when executed in Python without any scaling up technique.

<a id='12356c1c-ce17-4d6d-8642-240f02d216c6'></a>

## 4.5. Results and success stories
This algorithm has been run for a variety of categories, both General Merchandise and Fast-Moving Consumer Goods (like Yogurt, Light Bulbs, Dish Soap, Utility Pants, Food Storage, etc.) and has been seen to be performing really well.

<a id='1d5873db-4c85-4950-9ef4-eafddbb56782'></a>

The Mean Absolute Percentage Error for the model, when validated against observed assortment changes for the aforementioned categories, was almost always in the range of 4% to 13%.

<a id='b1af0393-d97b-47ac-bba0-b405357f1596'></a>

## 5. CONCLUSION
The problem of demand transference is an important one for any retailer. Obviously, the retailer cannot keep on carrying the same assortment over time. Market trends as well as the item performance, will always compel him to offer his customers the best assortment so as to maximize sales and customer satisfaction. Hence, it is better off to know from beforehand the magnitude of demand transference or cannibalization, that might be experienced with regards to a particular change in his assortment. Having a good understanding of the different scenarios will surely let him plan better than his competitors, and establish his stand in the market.

<a id='d1739f38-b630-42d0-9e6e-8447c1c80a69'></a>

Wrong choice of item deletion, might have severe repercussions in the form of:
1. churning of customer base which were loyal to the deleted product; or
2. churning of customer base, due to unavailability of proper substitutes of the deleted product in the available assortment.

<a id='9804c6e5-fcef-463f-9b39-f52edea775e2'></a>

Similarly, wrong choice of item addition could also be detrimental in the form of the new item not attracting any incremental demand of its own, but is only cannibalizing the demand of the other available items in the assortment, thus not doing any significant good to the retailer.

<a id='695b628f-5761-4e3a-9af5-733d4f7f4b09'></a>

This study has been aimed to help the retailer address these basic problems of assortment.

<a id='d410dcec-ab8f-4219-922c-c54f2e1a08c4'></a>

## 6. REFERENCES
Fishbein M, ed. (1967) *Attitude and Prediction of Behavior* (John Wiley & Sons, New York).
Fisher ML, Vaidyanathan R (2009) An Algorithm and Demand Estimation Procedure for Retail Assortment Optimization. The Wharton School, Philadelphia, Pennsylvania.
Goodall DW (1966) A new similarity index based on probability. *Biometrics* 22(4):882–907.

<a id='1ad9b7f2-cc2d-4893-87ba-3205ba788c63'></a>

Electronic copy available at: https://ssrn.com/abstract=3227753

<a id='663dba85-f344-4420-b996-f9804bcc44cd'></a>

Kök, G., M. L. Fisher. 2007. Demand Estimation and Assortment Optimization under
Substitution: Methodology and Application. Operations Research 55(6) 1001–1021.
Lancaster K (1971) Consumer Demand: A New Approach (Columbia University Press, New
York).

<a id='99e0b79a-2a2f-4fe9-8a3f-7030ea569259'></a>

Rooderkerk RP, van Heerde HJ, Bijmolt TH (2011) Optimizing Retail Assortments. *Marketing Science* 32(5):699–715.

<a id='fd25b771-c45c-44eb-b7ce-5831278811b4'></a>

Wittink DR, Addona MJ, Hawkes W, Porter JC (1988) SCAN*PRO:The estimation, validation, and use of promotional effects based on scanner data. Working paper, Cornell University, Ithaca, NY.

<a id='5585cb05-16f7-4dfb-ab1d-c9e06908633a'></a>

Electronic copy available at: https://ssrn.com/abstract=3227753