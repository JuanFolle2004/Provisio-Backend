<?php

declare(strict_types=1);

namespace Src\Groups\App\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;
use Src\Groups\Domain\Model\Group;

/**
 * @mixin Group
 */
class GroupResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'assignments_count' =>2,
            'products_count' => 2,
            'users_count' => 2,
        ];
    }
}
