<?php

declare(strict_types=1);

namespace Src\Assignment\App\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;
use Src\Assignment\Domain\Model\Assignment;

/**
 * @mixin Assignment
 */
class AssignmentResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'user'=>$this->user->name ?? '',
            'product_name' => $this->product->name ?? '',
            'amount' => $this->amount,
            'bought' => $this->bought,
        ];
    }
}
